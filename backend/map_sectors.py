import csv
from collections import defaultdict

sector_mapping = {
    'Information Technology': 'it',
    'Telecommunication': 'telecom',
    'Automobile and Auto Components': 'automobile',
    'Capital Goods': 'capital_goods',
    'Oil Gas & Consumable Fuels': 'energy',
    'Power': 'energy',
    'Healthcare': 'pharma',
    'Fast Moving Consumer Goods': 'fmcg',
    'Metals & Mining': 'metals',
    'Financial Services': 'finance',
    'Realty': 'realty',
    'Construction': 'realty',
    'Construction Materials': 'metals', # Or maybe keep it separate? We'll put it in metals/realty. Let's put in realty.
    'Chemicals': 'chemicals',
    'Consumer Services': 'hospitality',
    'Consumer Durables': 'hospitality',
    'Textiles': 'hospitality',
    'Services': 'hospitality'
}

sector_stocks = defaultdict(list)

# Read CSV and map
with open('../nifty.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        industry = row['Industry']
        symbol = row['Symbol'] + '.NS'
        sector = sector_mapping.get(industry, 'other')
        if sector != 'other':
            sector_stocks[sector].append(symbol)
            
# Print the results to be copy-pasted
with open('mapped.txt', 'w', encoding='utf-8') as out_f:
    for sector, stocks in sector_stocks.items():
        out_f.write(f"    '{sector}': [\n")
        stocks_str = "', '".join(stocks)
        out_f.write(f"        '{stocks_str}'\n")
        out_f.write("    ],\n")
