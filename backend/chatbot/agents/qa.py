"""
General Q&A Agent — answers finance questions.
3-Layer lookup pipeline:
  1. Question Bank (direct keyword match — instant, free)
  2. ChromaDB (semantic similarity — fast, free)
  3. Grok API via LangChain (only for unkown questions — uses API key)
"""
import os
import logging
from ..tools import (
    get_live_stock_price, 
    get_market_news_summary, 
    extract_stock_symbol,
    get_commodity_price,
    get_best_stock_in_sector,
    get_stocks_to_avoid,
    get_all_sector_picks
)

logger = logging.getLogger(__name__)


def _llm_answer(query: str, api_key: str) -> str | None:
    """Call Grok LLM only when the question is NOT in the question bank / ChromaDB."""
    try:
        from langchain_groq import ChatGroq
        from langchain.prompts import ChatPromptTemplate

        llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0.5)
        prompt = ChatPromptTemplate.from_messages([
            ('system', (
                "You are Zeus, an expert financial assistant for Indian and global markets. "
                "Answer concisely in under 200 words. Use emojis for readability. "
                "Specialise in: stocks, mutual funds, gold/silver, market analysis. "
                "If asked about yourself, say you are Zeus AI — a financial intelligence engine. "
                "If out of scope, redirect to finance topics politely."
            )),
            ('human', '{query}')
        ])
        chain = prompt | llm
        result = chain.invoke({'query': query})
        logger.info(f"Grok API used for query: '{query[:50]}'")
        return result.content.strip()
    except Exception as e:
        logger.warning(f"Grok Q&A failed: {e}")
        return None


def run(query: str, user_id: int | None = None) -> dict:
    """
    Answer a general finance question using the 4-layer pipeline.
    Layer 1: Direct stock price / news detection (no API needed)
    Layer 2: Question bank keyword lookup (instant)
    Layer 3: ChromaDB semantic similarity search (fast)
    Layer 4: Grok LLM API (only for unknown questions)
    """
    try:
        q = query.lower().strip()

        # ──────────────────────────────────────────────────────────────
        # LAYER 1: Direct stock price query
        # ──────────────────────────────────────────────────────────────
        try:
            symbol = extract_stock_symbol(query)
            if symbol and any(k in q for k in ['price', 'how much', 'cost', 'worth', 'trading', 'what is', 'rate', 'share price']):
                data = get_live_stock_price(symbol)
                price = data.get('price', 0)
                change_pct = data.get('change_pct', 0)
                currency = '₹' if '.NS' in symbol else '$'
                response = (
                    f"📈 **{symbol.replace('.NS', '')} Live Price**\n\n"
                    f"Price: **{currency}{price:,.2f}**\n"
                    f"Change: {change_pct:+.1f}% today\n"
                    f"*Updated: {data.get('timestamp', 'just now')}*"
                )
                return {'response': response, 'intent': 'qa'}
        except Exception as e:
            logger.warning(f"Layer 1 (Stock Price) failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 1B: Best Stock in Sector
        # ──────────────────────────────────────────────────────────────
        try:
            # Special Case: All Sectors / 14 Sectors
            if any(k in q for k in ['all sectors', '14 sectors', 'each sector', 'every sector']):
                response = get_all_sector_picks()
                return {'response': response, 'intent': 'qa'}

            if any(k in q for k in ['best stock', 'top performer', 'stocks in']):
                sectors = [
                    'it', 'banking', 'energy', 'pharma', 'auto', 'us', 
                    'fmcg', 'metal', 'realty', 'infra', 'media', 'chemicals', 
                    'psu bank', 'psu_bank', 'consumption', 'capital goods'
                ]
                import re
                for sector in sectors:
                    if re.search(rf'\b{sector}\b', q):
                        # Normalize names
                        clean_sector = sector
                        if sector == 'capital goods':
                            clean_sector = 'infra'
                        clean_sector = clean_sector.replace(' ', '_')
                        
                        response = get_best_stock_in_sector(clean_sector)
                        return {'response': response, 'intent': 'qa'}
                # Default to IT if no sector mentioned but best stock asked
                response = get_best_stock_in_sector('it')
                return {'response': response, 'intent': 'qa'}
        except Exception as e:
            logger.warning(f"Layer 1B (Best Stock) failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 1C: Commodity Price (Gold/Silver)
        # ──────────────────────────────────────────────────────────────
        try:
            if any(k in q for k in ['gold', 'silver', 'commodity', 'metal']):
                symbol = 'GC=F' if 'gold' in q else 'SI=F'
                data = get_commodity_price(symbol)
                response = (
                    f"🥇 **{data['symbol']} Live Tracker**\n\n"
                    f"Current Price: **{data['currency']}{data['price']:,}** per {data['unit']}\n"
                    f"Trend: {data['change_pct']:+.2f}% today\n"
                    f"*Source: {data.get('note', 'Market Data')}*"
                )
                return {'response': response, 'intent': 'qa'}
        except Exception as e:
            logger.warning(f"Layer 1B (Commodity) failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 1D: News query
        # ──────────────────────────────────────────────────────────────
        try:
            if any(k in q for k in ['news', 'latest', 'update', 'market today', 'headlines', 'what happened']):
                news = get_market_news_summary()
                import datetime
                response = f"📰 **Zeus Market News — {datetime.datetime.now().strftime('%d %b %Y')}**\n\n{news}\n\n*Insights generated by Zeus AI.*"
                return {'response': response, 'intent': 'qa'}
        except Exception as e:
            logger.warning(f"Layer 1D (News) failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 1E: Avoid Stocks (low reading stocks)
        # ──────────────────────────────────────────────────────────────
        try:
            if any(k in q for k in ['avoid', 'not buy', 'risky', 'low reading', 'falling', 'danger']):
                response = get_stocks_to_avoid()
                return {'response': response, 'intent': 'qa'}
        except Exception as e:
            logger.warning(f"Layer 1E (Avoid) failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 2: Question Bank (direct keyword lookup — free, instant)
        # ──────────────────────────────────────────────────────────────
        try:
            from ..question_bank import lookup_question_bank
            bank_answer = lookup_question_bank(query)
            if bank_answer:
                logger.info(f"Question bank hit for: '{q[:50]}'")
                return {'response': bank_answer, 'intent': 'qa', 'source': 'question_bank'}
        except Exception as e:
            logger.warning(f"Question bank lookup failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 3: ChromaDB Semantic Similarity (free, fast)
        # ──────────────────────────────────────────────────────────────
        try:
            from ..chroma_store import chroma_search
            chroma_answer = chroma_search(query)
            if chroma_answer:
                logger.info(f"ChromaDB hit for: '{q[:50]}'")
                return {'response': chroma_answer, 'intent': 'qa', 'source': 'chromadb'}
        except Exception as e:
            logger.warning(f"ChromaDB search failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 4: Grok LLM API (only for questions not in bank/ChromaDB)
        # ──────────────────────────────────────────────────────────────
        try:
            api_key = os.environ.get('GROQ_API_KEY')
            if api_key:
                llm_resp = _llm_answer(query, api_key)
                if llm_resp:
                    return {'response': llm_resp, 'intent': 'qa', 'source': 'grok_api'}
        except Exception as e:
            logger.warning(f"Layer 4 (Grok API) failed: {e}")

        # ──────────────────────────────────────────────────────────────
        # LAYER 5: Out-of-scope or generic fallback
        # ──────────────────────────────────────────────────────────────
        out_of_scope_kw = ['recipe', 'movie', 'game', 'sport', 'football', 'cricket score', 'weather', 'song']
        if any(k in q for k in out_of_scope_kw):
            return {
                'response': (
                    "🎯 **Out of Scope**\n\n"
                    "I specialise in finance. I can help you with:\n"
                    "• Stock analysis & recommendations\n"
                    "• Mutual funds & portfolio management\n"
                    "• Gold, silver & precious metals\n"
                    "• Market predictions & trends\n\n"
                    "*Try: \"What is RSI?\" or \"Suggest stocks for me\"*"
                ),
                'intent': 'qa'
            }

        return {
            'response': (
                "🧠 **Zeus AI**\n\n"
                "I'm here to help with your financial questions! Here's what I can do:\n"
                "• 📈 Live stock prices — *\"What is TCS price?\"*\n"
                "• 📊 Market concepts — *\"Explain P/E ratio\"*\n"
                "• 💼 Portfolio management — *\"Add Infosys to portfolio\"*\n"
                "• 🔮 Market predictions — *\"Forecast TCS for next month\"*\n"
                "• 🌟 Stock suggestions — *\"Suggest stocks for me\"*"
            ),
            'intent': 'qa'
        }

    except Exception as e:
        logger.error(f"Fatal error in QA agent: {e}", exc_info=True)
        return {
            'response': (
                "⚡ **Zeus AI Recovery Mode**\n\n"
                "I encountered an unexpected issue while processing your request. "
                "However, I'm still online! You can try asking about:\n"
                "• 📈 **Stock prices** (e.g., \"TCS price\")\n"
                "• 💼 **Your Portfolio**\n"
                "• 📰 **Market News**\n\n"
                "Please try your query again in a moment."
            ),
            'intent': 'error'
        }
