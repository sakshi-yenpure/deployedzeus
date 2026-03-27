"""
Recommendation Agent — suggests stocks based on user portfolio and market data.
"""
import os
import logging
from ..tools import get_sector_top_performers, get_user_portfolio, calculate_portfolio_risk

logger = logging.getLogger(__name__)


def _llm_recommend(query: str, context: str, api_key: str) -> str | None:
    try:
        from langchain_groq import ChatGroq
        from langchain.prompts import ChatPromptTemplate

        llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0.7)
        prompt = ChatPromptTemplate.from_messages([
            ('system', (
                "You are Zeus, an expert Indian stock market advisor. "
                "Provide concise, actionable stock recommendations. "
                "Always mention sector diversification and risk. "
                "Keep response under 200 words. Use emojis for readability.\n\n"
                "Market Context:\n{context}"
            )),
            ('human', '{query}')
        ])
        # Force string conversion to satisfy lint/runtime
        chain = prompt | llm
        result = chain.invoke({'query': query, 'context': context})
        return str(result.content).strip()
    except Exception as e:
        logger.warning(f"Groq recommendation failed: {e}")
        return None


def run(query: str, user_id: int | None = None) -> dict:
    """
    Generate stock recommendations.
    Returns: { 'response': str, 'intent': 'recommendation' }
    """
    try:
        q = query.lower()
        
        # --- Intent Filtering: Only proceed if it looks like a recommendation/risk/forecast query ---
        rec_keywords = [
            'suggest', 'recommend', 'pick', 'best stock', 'top performer', 'analysis', 
            'portfolio', 'risk', 'diversif', 'forecast', 'predict', 'trend', 'suggest',
            'should i buy', 'should i sell', 'growth', 'opportunity'
        ]
        if not any(k in q for k in rec_keywords):
            return {'response': None, 'intent': 'recommendation'}
        
        # Safe data fetching
        portfolio: list = []
        if user_id:
            try:
                portfolio = get_user_portfolio(user_id)
            except Exception as e:
                logger.warning(f"Portfolio fetch failed in recommendation agent: {e}")
        
        risk: dict = {'risk_level': 'N/A', 'score': 0, 'message': 'Risk analysis unavailable', 'sectors': []}
        try:
            risk = calculate_portfolio_risk(portfolio)
        except Exception as e:
            logger.warning(f"Risk calculation failed: {e}")

        # Determine sector focus from query
        sector = 'it'
        if any(k in q for k in ['bank', 'finance', 'financial']):
            sector = 'banking'
        elif any(k in q for k in ['pharma', 'health', 'medicine']):
            sector = 'pharma'
        elif any(k in q for k in ['energy', 'oil', 'power', 'reliance']):
            sector = 'energy'
        elif any(k in q for k in ['us', 'american', 'nasdaq', 's&p']):
            sector = 'us'

        top: list = []
        try:
            top = get_sector_top_performers(sector)
        except Exception as e:
            logger.warning(f"Sector top performers fetch failed: {e}")
            top = []

        # Build context for LLM
        portfolio_summary = ""
        if portfolio:
            symbols = [str(p.get('symbol', 'Unknown')).replace('.NS', '') for p in portfolio[:5]]
            portfolio_summary = f"User holds: {', '.join(symbols)}. Risk: {risk.get('risk_level', 'N/A')}."

        top_summary = "\n".join(
            [f"  • {str(s.get('symbol', 'Unknown')).replace('.NS', '')}: ₹{s.get('price', 0)} ({s.get('change_pct', 0):+.1f}%)" for s in top]
        )
        context = f"{portfolio_summary}\nTop {sector.upper()} performers:\n{top_summary}"

        api_key = os.environ.get('GROQ_API_KEY')
        llm_response = None
        if api_key:
            llm_response = _llm_recommend(query, context, api_key)

        if llm_response:
            return {'response': llm_response, 'intent': 'recommendation'}

        # — Fallback: structured response —
        is_risk_query = any(k in q for k in ['risk', 'diversif', 'level', 'safe'])

        if is_risk_query and portfolio:
            sectors_list = risk.get('sectors', [])
            sectors_str = ', '.join([str(s) for s in sectors_list])
            response = (
                f"📊 **Portfolio Risk Analysis**\n\n"
                f"Risk Level: **{risk.get('risk_level', 'N/A')}** (Score: {risk.get('score', 0)}/100)\n"
                f"Diversification: {risk.get('diversification', 0)} sector(s) — {sectors_str}\n\n"
                f"{risk.get('message', '')}\n\n"
                f"💡 *Tip: Aim for 5+ sectors to lower risk.*"
            )
        elif portfolio:
            held = [str(p.get('symbol', '')).replace('.NS', '') for p in portfolio[:3]]
            response = (
                f"🌟 **Top {sector.upper()} Picks for You**\n\n"
                + "\n".join([f"**{str(s.get('symbol', '')).replace('.NS','')}** — ₹{s.get('price', 0)} ({s.get('change_pct', 0):+.1f}%)" for s in top])
                + f"\n\n📌 You already hold: {', '.join(held)}.\n"
                f"💡 Consider diversifying into **{sector.upper()}** to balance your portfolio."
            )
        else:
            response = (
                f"🌟 **Top {sector.upper()} Stocks Right Now**\n\n"
                + "\n".join([f"**{str(s.get('symbol', '')).replace('.NS','')}** — ₹{s.get('price', 0)} ({s.get('change_pct', 0):+.1f}%)" for s in top])
                + "\n\n💡 *Log in to get personalized recommendations based on your portfolio.*"
            )

        return {'response': response, 'intent': 'recommendation'}

    except Exception as e:
        logger.error(f"Fatal error in recommendation agent: {e}", exc_info=True)
        return {
            'response': (
                "⚡ **Zeus AI Recommendation Fallback**\n\n"
                "I couldn't generate a personalized recommendation right now. "
                "However, I suggest focusing on large-cap leaders like **TCS**, **Reliance**, and **HDFC Bank** for stable long-term growth.\n\n"
                "Check the **Stocks** page for more detailed analytics!"
            ),
            'intent': 'recommendation'
        }
