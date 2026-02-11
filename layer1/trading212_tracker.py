"""
Trading212 Portfolio Tracker
Tells you exactly what to buy each week
"""

import yfinance as yf
from datetime import datetime
import json

class Trading212Tracker:
    def __init__(self, weekly_amount=100):
        # Your portfolio (customize these!)
        self.portfolio = {
            'VUSA.L': {'allocation': 0.30, 'name': 'S&P 500 ETF'},
            'VWRL.L': {'allocation': 0.25, 'name': 'All-World ETF'},
            'EQQQ.L': {'allocation': 0.25, 'name': 'Nasdaq 100 ETF'},
            'VHYL.L': {'allocation': 0.10, 'name': 'Dividend ETF'},
            'AAPL': {'allocation': 0.05, 'name': 'Apple'},
            'MSFT': {'allocation': 0.05, 'name': 'Microsoft'}
        }
        
        self.weekly_amount = weekly_amount
    
    def get_prices(self):
        """Fetch current prices"""
        print("\n📊 Fetching current prices...\n")
        
        prices = {}
        for ticker in self.portfolio.keys():
            try:
                stock = yf.Ticker(ticker)
                price = stock.history(period='1d')['Close'].iloc[-1]
                prices[ticker] = price
                print(f"✅ {ticker}: ${price:.2f}")
            except:
                print(f"⚠️  {ticker}: Could not fetch price")
                prices[ticker] = None
        
        return prices
    
    def calculate_buys(self):
        """Calculate what to buy this week"""
        
        print("\n" + "="*60)
        print(f"💰 WEEKLY INVESTMENT PLAN: ${self.weekly_amount}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
        print("="*60 + "\n")
        
        prices = self.get_prices()
        
        print("\n" + "="*60)
        print("📋 YOUR SHOPPING LIST:")
        print("="*60 + "\n")
        
        for ticker, config in self.portfolio.items():
            amount = self.weekly_amount * config['allocation']
            price = prices.get(ticker)
            
            if price:
                shares = amount / price
                print(f"{config['name']} ({ticker})")
                print(f"  💵 Invest: ${amount:.2f}")
                print(f"  📈 Current Price: ${price:.2f}")
                print(f"  📊 Buy: {shares:.4f} shares")
                print()
        
        print("="*60)
        print("✅ ACTION: Open Trading212 and execute these buys")
        print("⏱️  Time needed: ~5 minutes")
        print("="*60 + "\n")

# Run it
if __name__ == "__main__":
    tracker = Trading212Tracker(weekly_amount=100)
    tracker.calculate_buys()
