import yfinance as yf
import pandas as pd
import time
import os
from sqlconnect import get_sql_connection
from datetime import timedelta , datetime
conn = get_sql_connection()
cursor = conn.cursor()


last_cleanup_time = datetime.now()

cursor.execute("""
IF OBJECT_ID('dbo.StockLiveData', 'U') IS NULL
CREATE TABLE dbo.StockLiveData (
    [Symbol] VARCHAR(10),
    [Name] NVARCHAR(255),
    [Price] FLOAT,
    [MarketCap] BIGINT,
    [PERatio] FLOAT,
    [High52W] FLOAT,
    [Low52W] FLOAT,
    [Volume] BIGINT,
    [Sector] NVARCHAR(100),
    [FetchTime] DATETIME DEFAULT GETDATE()
)
""")
conn.commit()

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
            "Market_Cap": info.get("marketCap", ""),
            "PERatio": info.get("trailingPE", ""),
            "High52W": info.get("fiftyTwoWeekHigh", ""),
            "Low52W": info.get("fiftyTwoWeekLow", ""),
            "Volume": info.get("volume", ""),
            "Sector": info.get("sector", ""),
        }
        data.append(row)
        cursor.execute("""
                    INSERT INTO dbo.StockLiveData 
                    (Symbol, Name, Price, MarketCap, PERatio, High52W, Low52W, Volume, Sector)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row["Symbol"], row["Name"], row["Price"], row["Market_Cap"],
                    row["PERatio"], row["High52W"], row["Low52W"], row["Volume"], row["Sector"])

        conn.commit()

    df = pd.DataFrame(data)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(df.to_string(index=False))

def clean_data():
    print("deleting old stock data from SQL")
    cursor.execute("Truncate table dbo.StockLiveData ")
    conn.commit()



if __name__ == "__main__":
    while True:
        currtime = datetime.now()

        if (currtime - last_cleanup_time) >= timedelta(seconds=60):
            clean_data()
            last_cleanup_time = currtime


        fetch_and_display()
        print("\nUpdating in 60 seconds...")
        time.sleep(3600)

        