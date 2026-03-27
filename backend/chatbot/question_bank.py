"""
Comprehensive Question Bank for Zeus Chatbot.
Contains pre-written answers for common queries across:
- Greetings & small talk
- Finance concepts
- Portfolio topics
- Stock market questions
"""

# ──────────────────────────────────────────────────────────────────────
# CATEGORY 1: GREETINGS & SMALL TALK
# ──────────────────────────────────────────────────────────────────────
GREETINGS = {
    "hello": (
        "👋 **Hello! Welcome to Zeus AI!**\n\n"
        "I'm your personal financial intelligence engine. I can help you with:\n"
        "• 📈 Live stock prices and analysis\n"
        "• 💼 Portfolio management\n"
        "• 📊 Market concepts (P/E, RSI, Moving Averages)\n"
        "• 🔮 Market predictions and trends\n"
        "• 🥇 Metals (Gold, Silver) tracking\n\n"
        "*Try: \"What is TCS price?\" or \"Suggest stocks for me\"*"
    ),
    "hi": (
        "⚡ **Hi there!** Zeus AI is online and ready.\n\n"
        "What financial insights can I generate for you today?\n"
        "Ask me about stocks, portfolio, mutual funds, or market trends!"
    ),
    "hey": (
        "🚀 **Hey!** Zeus Core activated.\n\n"
        "I'm here to power your investment decisions. What would you like to explore?"
    ),
    "good morning": (
        "🌅 **Good Morning!**\n\n"
        "Markets open at 9:15 AM IST. Let's review your portfolio or check today's market outlook!\n"
        "Ask me: *\"What is today's market news?\"*"
    ),
    "good afternoon": (
        "☀️ **Good Afternoon!**\n\n"
        "Markets are active! Great time to review stocks and track live prices.\n"
        "What would you like to analyse?"
    ),
    "good evening": (
        "🌙 **Good Evening!**\n\n"
        "Markets have closed. Perfect time to review your portfolio performance and plan tomorrow's strategy!\n"
        "Ask me: *\"What is my portfolio risk level?\"*"
    ),
    "good night": (
        "🌟 **Good Night!**\n\n"
        "Rest well! Asian markets open early — remember that global cues impact Indian markets.\n"
        "Zeus AI will be here when you're ready to trade tomorrow. 💤"
    ),
    "bye": (
        "👋 **Goodbye!** Happy investing!\n\n"
        "Remember: *Invest regularly, diversify wisely, stay patient.* 📈\n"
        "Zeus AI is always here when you need financial intelligence."
    ),
    "goodbye": (
        "✅ **See you soon!**\n\n"
        "Keep tracking your portfolio and investments. 💼\n"
        "Zeus AI is always available — just open me anytime!"
    ),
    "thanks": (
        "😊 **You're welcome!**\n\n"
        "Happy to help with your financial journey. Feel free to ask me anything about markets, stocks, or your portfolio!"
    ),
    "thank you": (
        "🙏 **Anytime!** That's what Zeus AI is here for.\n\n"
        "Is there anything else you'd like to know about stocks or markets?"
    ),
    "how are you": (
        "✅ **All systems operational!** Zeus Core is running at full capacity.\n\n"
        "Markets are moving — shall we analyse some stocks or check your portfolio performance?"
    ),
    "what can you do": (
        "🧠 **Zeus AI Capabilities:**\n\n"
        "• 📈 **Live Prices** — Any stock, real-time\n"
        "• 💼 **Portfolio** — Add/remove stocks, view holdings\n"
        "• 📊 **Market Concepts** — P/E, RSI, MACD, SIP, etc.\n"
        "• 🔮 **Forecasting** — Price predictions with linear regression\n"
        "• 🌟 **Recommendations** — Personalised stock suggestions\n"
        "• 🥇 **Metals** — Gold & silver price tracking\n"
        "• 📰 **News** — Daily market headlines"
    ),
    "help": (
        "📋 **Zeus AI Help Guide**\n\n"
        "**Quick commands:**\n"
        "• *\"What is TCS price?\"* — Live stock price\n"
        "• *\"Add Infosys to my portfolio\"* — Portfolio management\n"
        "• *\"Suggest stocks for me\"* — AI recommendations\n"
        "• *\"What is P/E ratio?\"* — Learn finance concepts\n"
        "• *\"Forecast TCS for next month\"* — Price prediction\n"
        "• *\"What is today's market news?\"* — Daily headlines"
    ),
    "who are you": (
        "⚡ **I am Zeus AI** — your personal financial intelligence engine.\n\n"
        "Built for the Zeus investment platform, I specialise in:\n"
        "• Indian (NSE/BSE) and US stock markets\n"
        "• Real-time price fetching via yfinance\n"
        "• AI-powered recommendations using sentiment analysis\n"
        "• Portfolio management with MPIN security\n\n"
        "*Powered by advanced AI for smarter investing.*"
    ),
}

# ──────────────────────────────────────────────────────────────────────
# CATEGORY 1B: PLATFORM HELP
# ──────────────────────────────────────────────────────────────────────
PLATFORM_HELP = {
    "forgot password": (
        "🔑 **Forgot Password? No problem!**\n\n"
        "Follow these steps to recover your account:\n"
        "1. Go to the **Login** page.\n"
        "2. Click on the **'Forgot Password?'** link below the login button.\n"
        "3. Enter your **registered email address**.\n"
        "4. Check your inbox for a **reset link** (and your spam folder too!).\n"
        "5. Click the link and set a **new secure password**.\n\n"
        "*Tip: Use a mix of letters, numbers, and symbols!*"
    ),
    "reset password": (
        "🔄 **Password Reset Instructions:**\n\n"
        "You can change your password anytime in **Settings > Security** if you're logged in.\n"
        "If you can't log in, use the **'Forgot Password'** option on the login screen to receive a reset link via email."
    ),
    "is it secure": (
        "🛡️ **Security is our top priority!**\n\n"
        "Zeus AI uses enterprise-grade encryption and security protocols:\n"
        "• **JWT Authentication** for secure sessions\n"
        "• **MPIN Protection** for sensitive portfolio portfolio actions\n"
        "• **Encrypted database** for user credentials\n"
        "• **Secure API communication** (HTTPS)"
    ),
    "about zeus": (
        "🧠 **About Zeus AI — Your Financial Intelligence Engine**\n\n"
        "Zeus is a state-of-the-art financial platform designed to empower investors with AI-driven insights. Our core features include:\n"
        "• 📈 **Real-time Portfolio Tracking**: Monitor your investments across 14+ sectors.\n"
        "• 🔮 **ML Price Predictions**: Advanced linear regression models to forecast stock movements.\n"
        "• 🎯 **K-Means Clustering**: Visualize stock patterns and market segments.\n"
        "• 📊 **P/E Ratio Analytics**: Deep dive into valuation trends.\n"
        "• 📰 **Live Market News**: Stay updated with indexed headlines from global sources.\n\n"
        "Whether you are a day trader or a long-term investor, Zeus AI provides the data-driven edge you need."
    ),
    "signup steps": (
        "📝 **How to Join Zeus AI**\n\n"
        "Ready to start your financial journey? Here is how to create your account:\n"
        "1. Click the **'Get Started'** or **'Signup'** button on the Home page.\n"
        "2. Enter your **Full Name** and a valid **Email Address**.\n"
        "3. Choose a **Secure Password** (minimum 8 characters).\n"
        "4. Click **'Create Account'**.\n"
        "5. You will be redirected to your **Dashboard**, where you can start adding stocks to your portfolio!\n\n"
        "🚀 *Welcome to the future of investing!*"
    ),
    "login steps": (
        "🔑 **Accessing Your Zeus Dashboard**\n\n"
        "To log back into your account:\n"
        "1. Visit the **Login** page.\n"
        "2. Enter your **Registered Email**.\n"
        "3. Enter your **Password**.\n"
        "4. Click **'Login'**.\n\n"
        "💡 *Once logged in, your personalized portfolio and AI recommendations will be instantly available.*"
    ),
}

# ──────────────────────────────────────────────────────────────────────
# CATEGORY 2: FINANCE CONCEPTS
# ──────────────────────────────────────────────────────────────────────
FINANCE_CONCEPTS = {
    "pe ratio": (
        "📊 **P/E Ratio (Price-to-Earnings)**\n\n"
        "Shows how much you pay for ₹1 of a company's earnings.\n"
        "• **High P/E (>30):** Investors expect high growth, or overvalued.\n"
        "• **Low P/E (<15):** Could be undervalued or slow-growth.\n"
        "• **Rule:** Always compare P/E within the same sector.\n\n"
        "💡 *A P/E of 20-25 is fair for most Indian large-caps.*"
    ),
    "rsi": (
        "📉 **RSI — Relative Strength Index**\n\n"
        "Momentum indicator measuring speed of price movements (0–100).\n"
        "• **RSI < 30:** Oversold — potential buying opportunity 🛒\n"
        "• **RSI > 70:** Overbought — possible correction ⚠️\n"
        "• **RSI 40–60:** Neutral zone\n\n"
        "💡 *Best used alongside price charts and volume data.*"
    ),
    "moving average": (
        "📈 **Moving Averages (MA)**\n\n"
        "Smooths price data to identify trends.\n"
        "• **MA20:** 20-day average — short-term trend\n"
        "• **MA50:** 50-day average — medium-term trend\n"
        "• **MA200:** 200-day average — long-term trend\n"
        "• Price above MA20 → **Bullish signal** 🚀\n"
        "• *Golden cross (MA50 > MA200) = Strong buy signal*"
    ),
    "macd": (
        "📊 **MACD — Moving Average Convergence Divergence**\n\n"
        "Trend-following momentum indicator.\n"
        "• **MACD line crosses above Signal line** → Buy signal 🟢\n"
        "• **MACD line crosses below Signal line** → Sell signal 🔴\n"
        "• **Histogram above zero** → Bullish momentum\n\n"
        "💡 *MACD is best used in trending markets, not sideways ones.*"
    ),
    "sip": (
        "💰 **SIP — Systematic Investment Plan**\n\n"
        "Invest a fixed amount at regular intervals (monthly/weekly).\n"
        "• **Rupee-cost averaging:** Buy more units when prices fall\n"
        "• Minimum SIP: ₹100-500/month\n"
        "• Best for: Long-term wealth building (5-20 years)\n"
        "• Tax-saving ELSS SIPs qualify for 80C deduction\n\n"
        "💡 *₹5,000/month SIP for 20 years at 12% CAGR = ₹49 lakhs!*"
    ),
    "mutual fund": (
        "📦 **Mutual Funds**\n\n"
        "Pooled investment vehicles managed by fund managers.\n"
        "• **Equity funds:** Higher return, higher risk (5+ year horizon)\n"
        "• **Debt funds:** Stable returns, lower risk\n"
        "• **Index funds:** Low-cost, market-matching returns\n"
        "• **Hybrid funds:** Mix of equity and debt\n\n"
        "💡 *Index funds with expense ratio <0.5% beat most active funds long-term.*"
    ),
    "nifty": (
        "📊 **Nifty 50**\n\n"
        "India's benchmark stock index — tracks 50 largest NSE-listed companies.\n"
        "• Represents ~13 sectors and ~65% of NSE's market cap\n"
        "• Used to gauge overall Indian market health\n"
        "• Green Nifty → broad market up; Red Nifty → market down\n\n"
        "💡 *A Nifty 50 index fund gives instant diversification.*"
    ),
    "sensex": (
        "📊 **Sensex (S&P BSE Sensex)**\n\n"
        "BSE's benchmark index — tracks 30 largest Mumbai Stock Exchange companies.\n"
        "• India's oldest stock index (since 1986)\n"
        "• Reflects India's economic health\n"
        "• All-time high crossed 80,000 in 2024\n\n"
        "💡 *Sensex and Nifty usually move together — both represent India's top companies.*"
    ),
    "dividend": (
        "💵 **Dividends**\n\n"
        "Portion of company profits distributed to shareholders.\n"
        "• **Dividend yield:** Annual dividend / Stock price × 100\n"
        "• 2-4% yield is considered good for Indian stocks\n"
        "• High dividends = mature, cash-rich companies\n"
        "• Low dividends = growth companies reinvesting profits\n\n"
        "💡 *Top dividend stocks: Coal India, IOC, ONGC have high yields.*"
    ),
    "ipo": (
        "🏢 **IPO — Initial Public Offering**\n\n"
        "When a private company lists its shares publicly for the first time.\n"
        "• Apply via ASBA (bank) or UPI method\n"
        "• Allotment is lottery-based for oversubscribed IPOs\n"
        "• Grey market premium (GMP) hints at listing price\n"
        "• Lock-in period: Anchor investors 90 days\n\n"
        "💡 *Don't invest in IPOs blindly — always check financials and promoter background.*"
    ),
    "f&o": (
        "📋 **F&O — Futures & Options**\n\n"
        "Derivative instruments for hedging or speculation.\n"
        "• **Futures:** Agreement to buy/sell at future date at set price\n"
        "• **Options (Call):** Right to BUY at strike price\n"
        "• **Options (Put):** Right to SELL at strike price\n"
        "• High leverage = high risk + high reward\n\n"
        "⚠️ *F&O is for experienced traders only — 90% of retail traders lose money.*"
    ),
    "stop loss": (
        "🛡️ **Stop Loss**\n\n"
        "A pre-set price at which your trade automatically closes to limit losses.\n"
        "• Example: Buy TCS at ₹4,000, set stop-loss at ₹3,800 (5% loss limit)\n"
        "• Trailing stop loss adjusts with price movement\n"
        "• Always use stop losses in F&O and intraday trading\n\n"
        "💡 *Rule: Never risk more than 2% of your capital on a single trade.*"
    ),
    "market cap": (
        "🔢 **Market Capitalisation**\n\n"
        "Total market value of a company = Share Price × Total Shares.\n"
        "• **Large-cap (>₹20,000 Cr):** Stable, less volatile\n"
        "• **Mid-cap (₹5,000-20,000 Cr):** Growth potential, moderate risk\n"
        "• **Small-cap (<₹5,000 Cr):** High growth, high risk\n\n"
        "💡 *Nifty 50 stocks are all large-caps — considered safest for long-term.*"
    ),
    "eps": (
        "💹 **EPS — Earnings Per Share**\n\n"
        "Net profit divided by number of shares outstanding.\n"
        "• Higher EPS = more profitable company\n"
        "• Growing EPS over years = strong business\n"
        "• Used in combination with P/E (P/E = Price / EPS)\n\n"
        "💡 *Always compare EPS growth year-on-year for quality analysis.*"
    ),
    "book value": (
        "📚 **Book Value**\n\n"
        "Net assets per share = (Total Assets - Total Liabilities) / Shares.\n"
        "• **P/B Ratio < 1:** Stock trading below book value (potentially undervalued)\n"
        "• **P/B Ratio > 3:** Premium valuation (growth stock)\n\n"
        "💡 *P/B Ratio is best used for banking and financial stocks.*"
    ),
    "intraday": (
        "⚡ **Intraday Trading**\n\n"
        "Buying and selling stocks within the same trading day (9:15 AM - 3:30 PM IST).\n"
        "• Positions must be closed before market close\n"
        "• High leverage available (up to 5x)\n"
        "• Requires more capital monitoring and discipline\n\n"
        "⚠️ *80% of intraday traders lose money. Not recommended for beginners.*"
    ),
    "demat": (
        "🏦 **Demat Account**\n\n"
        "Dematerialised account — holds your shares in electronic form.\n"
        "• Required to buy/sell stocks in India\n"
        "• Linked with your trading (broker) account\n"
        "• Annual charges: ₹0–₹500 depending on broker\n"
        "• Popular brokers: Zerodha, Groww, Angel One, HDFC Sky\n\n"
        "💡 *Open with a discount broker for minimal charges.*"
    ),
    "portfolio": (
        "💼 **Your Investment Portfolio**\n\n"
        "A collection of all your investment holdings.\n"
        "• Diversification reduces risk — invest across sectors\n"
        "• Recommended split: 70% equity, 20% debt, 10% gold\n"
        "• Review portfolio every quarter\n"
        "• Rebalance annually to maintain target allocation\n\n"
        "💡 *Use Zeus to track your portfolio performance and get AI insights!*"
    ),
}

# ──────────────────────────────────────────────────────────────────────
# CATEGORY 3: STOCK SPECIFIC
# ──────────────────────────────────────────────────────────────────────
STOCK_CONCEPTS = {
    "tcs": (
        "💼 **Tata Consultancy Services (TCS)**\n\n"
        "India's largest IT services company by market cap.\n"
        "• NSE Symbol: TCS.NS\n"
        "• Revenue: ~$29 billion (FY24)\n"
        "• Business: IT outsourcing, consulting, digital transformation\n"
        "• Global clients: 65+ Fortune 500 companies\n\n"
        "💡 *Ask me: \"What is TCS price today?\"*"
    ),
    "infosys": (
        "💻 **Infosys (INFY)**\n\n"
        "India's second-largest IT company, known for AI and automation.\n"
        "• NSE Symbol: INFY.NS | NYSE: INFY\n"
        "• Revenue: ~$18 billion (FY24)\n"
        "• Business: Enterprise software, cloud, consulting\n"
        "• Founded by Narayan Murthy in 1981\n\n"
        "💡 *Ask me: \"What is Infosys price?\"*"
    ),
    "reliance": (
        "⛽ **Reliance Industries (RELIANCE)**\n\n"
        "India's most valuable company across sectors.\n"
        "• NSE Symbol: RELIANCE.NS\n"
        "• Market Cap: ~₹20 lakh crore\n"
        "• Business: Telecom (Jio), Retail, Petrochemicals, Green Energy\n"
        "• Dividend-paying large-cap stock\n\n"
        "💡 *Ask me: \"What is Reliance price?\"*"
    ),
    "sector": (
        "🏭 **Market Sectors**\n\n"
        "Zeus tracks these sectors on the platform:\n"
        "• 💻 **IT** — TCS, Infosys, HCL Tech\n"
        "• 🏦 **Banking** — HDFC, ICICI, SBI\n"
        "• ⛽ **Energy** — Reliance, NTPC, ONGC\n"
        "• 💊 **Pharma** — Sun Pharma, Cipla, Dr Reddy's\n"
        "• 🚗 **Auto** — Tata Motors, Maruti, Bajaj Auto\n"
        "• 🏗️ **Capital Goods** — L&T, Siemens, ABB\n\n"
        "💡 *Visit the Stocks page to explore all sectors!*"
    ),
    "gold": (
        "🥇 **Gold Market**\n\n"
        "Gold is the ultimate safe-haven asset.\n"
        "• Rises during inflation, geopolitical uncertainty, or weak USD\n"
        "• Current spot: ~$3,000/oz (MCX: ~₹90,000/10g)\n"
        "• Ideal portfolio allocation: 5–10%\n"
        "• Track it on Zeus's **Metals** page with RSI & MA charts.\n\n"
        "💡 *Gold doesn't pay dividends but protects purchasing power.*"
    ),
    "silver": (
        "🥈 **Silver Market**\n\n"
        "Silver has dual demand — investment + industrial use.\n"
        "• ~70% of demand comes from industry (EVs, solar panels)\n"
        "• Current spot: ~$33/oz (MCX: ~₹95,000/kg)\n"
        "• More volatile than gold — higher risk, higher reward\n\n"
        "💡 *Silver often outperforms gold in bull markets.*"
    ),
    "large cap": (
        "🏢 **Large-Cap Stocks**\n\n"
        "Market cap above ₹20,000 crore — India's biggest companies.\n"
        "• Stable, less volatile than mid/small caps\n"
        "• Examples: TCS, Reliance, HDFC Bank, Infosys\n"
        "• Best for: Conservative investors, long-term holding\n"
        "• Lower risk, steady returns (12-15% CAGR historically)\n\n"
        "💡 *Nifty 50 = top 50 large-cap stocks.*"
    ),
    "small cap": (
        "🚀 **Small-Cap Stocks**\n\n"
        "Market cap below ₹5,000 crore — smaller companies.\n"
        "• Higher growth potential but more volatile\n"
        "• Can 10x in strong bull markets\n"
        "• Higher risk of delisting or losses in bear markets\n\n"
        "⚠️ *Only invest money you can afford to lose in small-caps.*"
    ),
    "best stock in it": "I can help you find the **best stock in the IT sector**! Just ask: *\"What is the best stock in IT?\"*",
    "best stock in banking": "I can help you find the **best stock in Banking**! Just ask: *\"What is the best stock in Banking?\"*",
    "best stock in auto": "I can help you find the **best stock in Auto**! Just ask: *\"What is the best stock in Auto?\"*",
    "best stock in pharma": "I can help you find the **best stock in Pharma**! Just ask: *\"What is the best stock in Pharma?\"*",
    "best stock in healthcare": "I can help you find the **best stock in Pharma** (Healthcare)!",
}

# ──────────────────────────────────────────────────────────────────────
# BUILD UNIFIED KNOWLEDGE BASE
# ──────────────────────────────────────────────────────────────────────

# Flat list of (question_text, answer_text) for ChromaDB indexing
ALL_QA_PAIRS: list[tuple[str, str]] = []

CATEGORY_GREETINGS_KEYS = set(GREETINGS.keys())
CATEGORY_CONCEPT_KEYS = set(FINANCE_CONCEPTS.keys())
CATEGORY_STOCK_KEYS = set(STOCK_CONCEPTS.keys())

for k, v in GREETINGS.items():
    ALL_QA_PAIRS.append((k, v))

for k, v in PLATFORM_HELP.items():
    ALL_QA_PAIRS.append((k, v))

for k, v in FINANCE_CONCEPTS.items():
    ALL_QA_PAIRS.append((k, v))

for k, v in STOCK_CONCEPTS.items():
    ALL_QA_PAIRS.append((k, v))


def lookup_question_bank(query: str) -> str | None:
    """
    Direct keyword lookup against the question bank.
    Returns the answer string if a match is found, else None.
    """
    q = query.lower().strip()

    # Check greetings first (full match)
    for key, answer in GREETINGS.items():
        if key in q or q in key:
            return answer

    # Check platform help (more flexible matching: all words must be present)
    for key, answer in PLATFORM_HELP.items():
        words = key.split()
        if all(w in q for w in words):
            return answer

    # Check finance concepts
    for key, answer in FINANCE_CONCEPTS.items():
        if key in q:
            return answer

    # Check stock concepts
    for key, answer in STOCK_CONCEPTS.items():
        if key in q:
            return answer

    return None
