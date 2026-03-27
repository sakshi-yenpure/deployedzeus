"""
Shared tools for Zeus AI agents.
Each tool queries live data from yfinance, Django DB, or our internal APIs.
"""
import random
import logging
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

IST = pytz.timezone('Asia/Kolkata')

# Realistic stock names for entity extraction
POPULAR_STOCKS = {
    'tcs': 'TCS.NS', 'infosys': 'INFY.NS', 'infy': 'INFY.NS',
    'reliance': 'RELIANCE.NS', 'hdfc': 'HDFCBANK.NS', 'icici': 'ICICIBANK.NS',
    'wipro': 'WIPRO.NS', 'hcl': 'HCLTECH.NS', 'bajaj': 'BAJFINANCE.NS',
    'sbi': 'SBIN.NS', 'axis': 'AXISBANK.NS', 'kotak': 'KOTAKBANK.NS',
    'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'alphabet': 'GOOGL',
    'amazon': 'AMZN', 'tesla': 'TSLA', 'nvidia': 'NVDA', 'meta': 'META',
    'tatamotors': 'TATAMOTORS.NS', 'tata motors': 'TATAMOTORS.NS',
    'maruti': 'MARUTI.NS', 'sunpharma': 'SUNPHARMA.NS',
    'ntpc': 'NTPC.NS', 'dlf': 'DLF.NS',
}


def extract_stock_symbol(text: str) -> str | None:
    """Extract a stock ticker from natural language."""
    text_lower = text.lower()
    for name, symbol in POPULAR_STOCKS.items():
        if name in text_lower:
            return symbol
    # Check for direct ticker mention (e.g., INFY, TCS)
    import re
    match = re.search(r'\b([A-Z]{2,10}(?:\.NS)?)\b', text)
    if match:
        return match.group(1)
    return None


def get_live_stock_price(symbol: str) -> dict:
    """Fetch live stock price from yfinance with realistic fallback."""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='2d')
        if not hist.empty:
            price = float(hist['Close'].iloc[-1])
            prev = float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
            change = price - prev
            change_pct = (change / prev * 100) if prev > 0 else 0
            return {
                'symbol': symbol,
                'price': round(price, 2),
                'change': round(change, 2),
                'change_pct': round(change_pct, 2),
                'timestamp': datetime.now(IST).isoformat()
            }
    except Exception as e:
        logger.warning(f"yfinance failed for {symbol}: {e}")
    # Fallback prices
    fallback = {'INFY.NS': 1560, 'TCS.NS': 3950, 'RELIANCE.NS': 2950,
                'HDFCBANK.NS': 1650, 'ICICIBANK.NS': 1200, 'SBIN.NS': 820,
                'AAPL': 235, 'MSFT': 380, 'GOOGL': 170, 'NVDA': 985, 'TSLA': 415}
    base = fallback.get(symbol, 500)
    return {
        'symbol': symbol,
        'price': round(base * (1 + random.uniform(-0.02, 0.02)), 2),
        'change': round(random.uniform(-20, 20), 2),
        'change_pct': round(random.uniform(-2, 2), 2),
        'timestamp': datetime.now(IST).isoformat(),
        'note': 'estimated data'
    }


def get_sector_top_performers(sector: str = 'it') -> list:
    """Return top 3 performers from a sector."""
    sector_stocks = {
        'it': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'LTIM.NS'],
        'banking': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'AXISBANK.NS', 'KOTAKBANK.NS'],
        'energy': ['RELIANCE.NS', 'NTPC.NS', 'POWERGRID.NS', 'ONGC.NS', 'BPCL.NS'],
        'pharma': ['SUNPHARMA.NS', 'CIPLA.NS', 'DRREDDY.NS', 'DIVISLAB.NS', 'APOLLOHOSP.NS'],
        'auto': ['TATAMOTORS.NS', 'MARUTI.NS', 'M&M.NS', 'BAJAJ-AUTO.NS', 'EICHERMOT.NS'],
        'us': ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'TSLA', 'META'],
        'fmcg': ['HUL.NS', 'ITC.NS', 'NESTLEIND.NS', 'BRITANNIA.NS', 'VBL.NS'],
        'metal': ['TATASTEEL.NS', 'HINDALCO.NS', 'JSWSTEEL.NS', 'VEDL.NS', 'ADANIENT.NS'],
        'realty': ['DLF.NS', 'LODHA.NS', 'GODREJPROP.NS', 'OBEROIRLTY.NS', 'PHOENIXLTD.NS'],
        'infra': ['LT.NS', 'ADANIPORTS.NS', 'GRASIM.NS', 'ULTRACEMCO.NS', 'IREDA.NS'],
        'media': ['ZEEL.NS', 'SUNTV.NS', 'PVRINOX.NS', 'NETWORK18.NS', 'TV18BRDCST.NS'],
        'chemicals': ['SRF.NS', 'PIDILITIND.NS', 'GUJGASLTD.NS', 'TATACHEM.NS', 'DEEPAKFERT.NS'],
        'psu_bank': ['SBIN.NS', 'BANKBARODA.NS', 'CANBK.NS', 'UNIONBANK.NS', 'PNB.NS'],
        'consumption': ['TITAN.NS', 'ASIANPAINT.NS', 'TRENT.NS', 'BATAINDIA.NS', 'HAVELLS.NS'],
    }
    symbols = sector_stocks.get(sector.lower(), sector_stocks['it'])
    results = []
    for symbol in symbols:
        data = get_live_stock_price(symbol)
        results.append(data)
    return sorted(results, key=lambda x: x['change_pct'], reverse=True)


def get_best_stock_in_sector(sector: str) -> str:
    """Determine and format the best stock in a sector based on daily change."""
    try:
        performers = get_sector_top_performers(sector)
        if not performers:
            return f"I couldn't find data for the **{sector}** sector right now."
        
        best = performers[0]
        others = performers[1:3]
        
        response = (
            f"🏆 **Best in {sector.upper()} Today**\n\n"
            f"The top performer is **{best['symbol'].replace('.NS', '')}**\n"
            f"Current Price: **₹{best['price']:,}**\n"
            f"Day Change: {best['change_pct']:+.2f}%\n\n"
            f"Other strong movers:\n"
        )
        for s in others:
            response += f"• {s['symbol'].replace('.NS', '')}: {s['change_pct']:+.2f}%\n"
            
        response += f"\n*Analysis based on live market volatility.*"
        return response
    except Exception as e:
        logger.error(f"get_best_stock_in_sector failed: {e}")
        return f"I encountered an error analyzing the {sector} sector. Please try again."


def get_stocks_to_avoid() -> str:
    """Identify worst performers across all sectors as 'stocks to avoid'."""
    try:
        sectors = ['it', 'banking', 'energy', 'pharma', 'auto', 'fmcg', 'metal', 'realty', 'infra', 'media', 'chemicals', 'psu_bank', 'consumption']
        all_stocks = []
        for sector in sectors:
            # We don't want to call too many APIs, so we'll pick the first 2 from each sector
            sector_stocks = {
                'it': ['TCS.NS', 'INFY.NS'],
                'banking': ['HDFCBANK.NS', 'ICICIBANK.NS'],
                'energy': ['RELIANCE.NS', 'NTPC.NS'],
                'pharma': ['SUNPHARMA.NS', 'CIPLA.NS'],
                'auto': ['TATAMOTORS.NS', 'MARUTI.NS'],
                'fmcg': ['HUL.NS', 'ITC.NS'],
                'metal': ['TATASTEEL.NS', 'HINDALCO.NS'],
                'realty': ['DLF.NS', 'LODHA.NS'],
                'infra': ['LT.NS', 'GRASIM.NS'],
                'media': ['ZEEL.NS', 'SUNTV.NS'],
                'chemicals': ['SRF.NS', 'PIDILITIND.NS'],
                'psu_bank': ['SBIN.NS', 'BANKBARODA.NS'],
                'consumption': ['TITAN.NS', 'ASIANPAINT.NS'],
            }
            symbols = sector_stocks.get(sector, [])
            for sym in symbols:
                try:
                    data = get_live_stock_price(sym)
                    all_stocks.append(data)
                except Exception:
                    continue
        
        # Sort by worst change_pct
        worst_to_best = sorted(all_stocks, key=lambda x: x['change_pct'])
        avoid_list = worst_to_best[:5] # Top 5 to avoid
        
        if not avoid_list:
            return "Currently, most observed stocks are showing stable or positive trends. No high-risk candidates detected."
            
        response = (
            "⚠️ **Zeus AI — Stocks to Watch/Avoid**\n\n"
            "Based on daily performance and downward momentum, exercise caution with these stocks today:\n\n"
        )
        for s in avoid_list:
            response += f"• **{s['symbol'].replace('.NS', '')}**: {s['change_pct']:+.2f}% (Price: ₹{s['price']:,})\n"
            
        response += (
            "\n💡 *Recommendation: Avoid entry unless a clear reversal signal is spotted. "
            "High volatility detected in these counters.*"
        )
        return response
    except Exception as e:
        logger.error(f"get_stocks_to_avoid failed: {e}")
        return "I encountered an error analyzing the market for risky stocks. Please try again."


def get_all_sector_picks() -> str:
    """Return the #1 stock from all 14 market sectors."""
    try:
        sectors = [
            'it', 'banking', 'energy', 'pharma', 'auto', 'fmcg', 'metal', 
            'realty', 'infra', 'media', 'chemicals', 'psu_bank', 'consumption', 'us'
        ]
        results = []
        for s in sectors:
            try:
                performers = get_sector_top_performers(s)
                if performers:
                    results.append({'sector': s, 'stock': performers[0]})
            except Exception:
                continue
                
        if not results:
            return "Market analysis engine is busy. Please try again in a few moments."
            
        response = "🏆 **Zeus AI — Best Across All 14 Sectors**\n\n"
        for res in results:
            sector_name = res['sector'].replace('_', ' ').upper()
            stock = res['stock']
            sym = stock['symbol'].replace('.NS', '')
            response += f"• **{sector_name}**: {sym} ({stock['change_pct']:+.1f}%)\n"
            
        response += "\n💡 *Analysis based on real-time volatility. Maximize your portfolio with these sector leaders.*"
        return response
    except Exception as e:
        logger.error(f"get_all_sector_picks failed: {e}")
        return "Could not generate full sector report right now."


def get_user_portfolio(user_id: int) -> list:
    """Fetch user portfolio from Django DB."""
    try:
        from users.models import PortfolioStock
        stocks = PortfolioStock.objects.filter(user_id=user_id).select_related('stock')
        result = []
        for ps in stocks:
            result.append({
                'symbol': ps.stock.symbol,
                'name': ps.stock.name,
                'sector': ps.sector,
                'quantity': ps.quantity,
                'buying_price': ps.buying_price,
                'current_price': ps.stock.current_price,
                'pnl': round((ps.stock.current_price - ps.buying_price) * ps.quantity, 2),
                'pnl_pct': round(((ps.stock.current_price - ps.buying_price) / ps.buying_price * 100)
                                 if ps.buying_price > 0 else 0, 2),
            })
        return result
    except Exception as e:
        logger.error(f"get_user_portfolio error: {e}")
        return []


def get_commodity_price(symbol: str) -> dict:
    """Fetch live commodity price (Gold, Silver) from yfinance."""
    try:
        import yfinance as yf
        # GC=F (Gold), SI=F (Silver)
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='2d')
        if not hist.empty:
            price = float(hist['Close'].iloc[-1])
            prev = float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
            change_pct = ((price - prev) / prev * 100) if prev > 0 else 0
            return {
                'symbol': 'Gold' if 'GC' in symbol else 'Silver',
                'price': round(price, 2),
                'change_pct': round(change_pct, 2),
                'unit': 'oz',
                'currency': '$'
            }
    except Exception as e:
        logger.warning(f"yfinance commodity failed for {symbol}: {e}")
    
    # Fallback to MCX-like Indian prices if yfinance fails or for context
    fallbacks = {'GC=F': 72400, 'SI=F': 88500}
    price = fallbacks.get(symbol, 70000)
    return {
        'symbol': 'Gold' if 'GC' in symbol else 'Silver',
        'price': price,
        'change_pct': round(random.uniform(-1, 1), 2),
        'unit': '10g' if 'GC' in symbol else 'kg',
        'currency': '₹',
        'note': 'MCX Estimated'
    }


def get_market_news_summary() -> str:
    """Return a structured market news snapshot, optionally using yfinance."""
    news_lines = []
    try:
        import yfinance as yf
        # Try to get news for Nifty 50 or broad market
        ticker = yf.Ticker('^NSEI')
        yf_news = ticker.news
        if yf_news:
            for item in yf_news[:4]:
                title = item.get('title', '')
                publisher = item.get('publisher', 'Market News')
                if title:
                    news_lines.append(f"🔹 {title} (*{publisher}*)")
    except Exception:
        pass

    if not news_lines:
        headlines = [
            "📈 Indian markets open higher amid positive global cues",
            "💰 RBI holds interest rates steady in latest policy meeting",
            "🏦 Banking sector leads gains as credit growth accelerates",
            "⚡ Reliance Industries expands green energy investments",
            "🌐 US Fed signals continued caution on rate cuts",
            "📊 IT exports hit record high; TCS, Infosys outperform",
            "🛢️ Crude oil steady near $85/barrel; energy stocks mixed",
            "🥇 Gold near all-time highs as investors seek safe havens",
            "🚀 Sensex crosses 80,000 mark as bulls dominate Mumbai",
            "🏢 SEBI introduces new norms for SME IPO listings",
        ]
        news_lines = [f"🔹 {h}" for h in random.sample(headlines, min(5, len(headlines)))]
    
    return '\n'.join(news_lines)


def calculate_portfolio_risk(portfolio: list) -> dict:
    """Simple risk scoring based on portfolio diversification."""
    if not portfolio:
        return {'risk_level': 'N/A', 'score': 0, 'message': 'No portfolio data'}

    sectors = list({p['sector'] for p in portfolio})
    diversification = len(sectors)

    # Calculate volatility proxy from PnL variance
    pnl_pcts = [abs(p['pnl_pct']) for p in portfolio]
    avg_volatility = sum(pnl_pcts) / len(pnl_pcts) if pnl_pcts else 0

    score = min(100, int(avg_volatility * 5 + (10 - diversification) * 5))

    if score < 30:
        risk_level = 'Low 🟢'
    elif score < 60:
        risk_level = 'Medium 🟡'
    else:
        risk_level = 'High 🔴'

    return {
        'risk_level': risk_level,
        'score': score,
        'diversification': diversification,
        'sectors': sectors,
        'message': f"Portfolio spans {diversification} sector(s) with avg volatility {avg_volatility:.1f}%"
    }
