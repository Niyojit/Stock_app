import yfinance as yf
import pandas as pd
import time
import os

# List of top 20 stock symbols (example: S&P 500 top 20 by market cap)
top_20_symbols = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "LLY", "JPM",
    "V", "UNH", "AVGO", "WMT", "MA", "XOM", "PG", "JNJ", "COST", "HD","TMC"
]

def fetch_and_display():
    stocks = yf.Tickers(" ".join(top_20_symbols))
    data = []
    for symbol in top_20_symbols:
        info = stocks.tickers[symbol].info
        row = {
            "Symbol": symbol,
            "Name": info.get("longName", ""),
            "Price": info.get("regularMarketPrice", ""),
            "Market Cap": info.get("marketCap", ""),
            "PE Ratio": info.get("trailingPE", ""),
            "52w High": info.get("fiftyTwoWeekHigh", ""),
            "52w Low": info.get("fiftyTwoWeekLow", ""),
            "Volume": info.get("volume", ""),
            "Sector": info.get("sector", ""),
        }
        data.append(row)
    df = pd.DataFrame(data)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(df.to_string(index=False))

if __name__ == "__main__":
    while True:
        fetch_and_display()
        print("\nUpdating in 60 seconds...")
        time.sleep(60)

        