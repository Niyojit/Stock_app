import yfinance as yf
import pandas as pd
import time
import os
from sqlconnect import get_sql_connection

conn = get_sql_connection()
cursor = conn.cursor()

cursor.execute("""
IF OBJECT_ID('dbo.IndianStockLiveData', 'U') IS NULL
CREATE TABLE dbo.IndianStockLiveData (
    [Symbol] VARCHAR(20),
    [Name] NVARCHAR(500),
    [Price] FLOAT,
    [MarketCap] BIGINT,
    [PERatio] FLOAT,
    [High52W] FLOAT,
    [Low52W] FLOAT,
    [Volume] BIGINT,
    [Sector] NVARCHAR(200),
    [FetchTime] DATETIME DEFAULT GETDATE()
)
""")

conn.commit()

# List of top 20 stock symbols (example: S&P 500 top 20 by market cap)
top_20_symbols = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "AXISBANK.NS", "LT.NS", "ITC.NS", "HINDUNILVR.NS",
    "BHARTIARTL.NS", "ASIANPAINT.NS", "BAJFINANCE.NS", "KOTAKBANK.NS",
    "MARUTI.NS", "HCLTECH.NS", "SUNPHARMA.NS", "WIPRO.NS", "POWERGRID.NS", "NTPC.NS"
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
            "Market_Cap": info.get("marketCap", ""),
            "PERatio": info.get("trailingPE", ""),
            "High52W": info.get("fiftyTwoWeekHigh", ""),
            "Low52W": info.get("fiftyTwoWeekLow", ""),
            "Volume": info.get("volume", ""),
            "Sector": info.get("sector", ""),
        }
        data.append(row)
        cursor.execute("""
                    INSERT INTO dbo.IndianStockLiveData 
                    (Symbol, Name, Price, MarketCap, PERatio, High52W, Low52W, Volume, Sector)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row["Symbol"], row["Name"], row["Price"], row["Market_Cap"],
                    row["PERatio"], row["High52W"], row["Low52W"], row["Volume"], row["Sector"])

        conn.commit()

    df = pd.DataFrame(data)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(df.to_string(index=False))


if __name__ == "__main__":
    while True:
    
        fetch_and_display()
        print("\nUpdating in 60 seconds...")
        time.sleep(10)

        