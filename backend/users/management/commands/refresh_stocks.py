from django.core.management.base import BaseCommand
import yfinance as yf
from users.models import Stock

class Command(BaseCommand):
    help = 'Refresh all stock prices from yfinance'

    def handle(self, *args, **kwargs):
        stocks = Stock.objects.all()
        updated = 0
        for stock in stocks:
            try:
                ticker = yf.Ticker(stock.symbol)
                info = ticker.fast_info
                hist = ticker.history(period='2d')
                stock.current_price = info.last_price or 0
                stock.day_high = info.day_high or 0
                stock.day_low = info.day_low or 0
                stock.volume = info.last_volume or 0
                stock.market_cap = info.market_cap or 0
                if len(hist) >= 2:
                    prev_close = hist['Close'].iloc[-2]
                    curr = info.last_price or 0
                    stock.change = curr - prev_close
                    stock.change_percent = ((curr - prev_close) / prev_close) * 100
                stock.save()
                updated += 1
            except Exception as e:
                self.stdout.write(f'Failed {stock.symbol}: {e}')
        self.stdout.write(f'Updated {updated} stocks')
