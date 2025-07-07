import yfinance as yf
import pandas as pd
from sqlconnect import get_sql_connection
from datetime import datetime, timedelta
import os
import sys
import time
import pytz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

top_20_symbols = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "AXISBANK.NS", "LT.NS", "ITC.NS", "HINDUNILVR.NS",
    "BHARTIARTL.NS", "ASIANPAINT.NS", "BAJFINANCE.NS", "KOTAKBANK.NS",
    "MARUTI.NS", "HCLTECH.NS", "SUNPHARMA.NS", "WIPRO.NS", "POWERGRID.NS", "NTPC.NS"
]

def fetch_and_store_halfhourly_data():
    conn = get_sql_connection()
    cursor = conn.cursor()

    cursor.execute("""
    IF OBJECT_ID('dbo.HistoryStockData', 'U') IS NULL
    CREATE TABLE dbo.HistoryStockData(
        [Symbol] VARCHAR(20),
        [Price] FLOAT,
        [DateTime] DATETIME,
        [Open] FLOAT,
        [High] FLOAT,
        [Low] FLOAT,
        [Close] FLOAT,
        [Volume] BIGINT
    )
    """)
    conn.commit()

    tz = pytz.timezone("Asia/Kolkata")

# Convert to timezone-aware datetime
    now = datetime.now(tz)
    one_hour_ago = now - timedelta(hours=1)
   
    for symbol in top_20_symbols:
        print(f"Fetching data for last 1 hour at 30-minute intervals: {symbol}")
        stock = yf.Ticker(symbol)
        df = stock.history(period="1d", interval="30m")

        if df.empty:
            print(f"No data returned for {symbol}")
            continue

        df = df.reset_index()
       
        df["Datetime"] = pd.to_datetime(df["Datetime"])

        df_last_hour = df[df["Datetime"] >= one_hour_ago].tail(2)

        for _, row in df_last_hour.iterrows():
            
            cursor.execute("""
                SELECT COUNT(*) FROM dbo.HistoryStockData
                WHERE Symbol = ? AND DateTime = ?
            """, symbol, row["Datetime"])
            exists = cursor.fetchone()[0]

            if exists == 0:
                cursor.execute("""
                    INSERT INTO dbo.HistoryStockData
                    (Symbol, Price, DateTime, [Open], High, Low, [Close], Volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, symbol, row["Close"], row["Datetime"], row["Open"], row["High"],
                     row["Low"], row["Close"], row["Volume"])
            else:
                print(f"Skipping duplicate for {symbol} at {row['Datetime']}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    while True:
        print(f"\n⏰ Fetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        fetch_and_store_halfhourly_data()
        print("✅ Done. Waiting for 30 minutes...\n")
        time.sleep(1800)
