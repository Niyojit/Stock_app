import yfinance as yf
import pandas as pd
from sqlconnect import get_sql_connection
from datetime import datetime
import os
import sys
import time
from streamlit_autorefresh import st_autorefresh
# Add parent directory to sys.path
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
    st_autorefresh(interval=3000, key="refresh_explore")
    # Create the table if not exists
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

    for symbol in top_20_symbols:
        print(f"Fetching 30-min interval data for past 10 days: {symbol}")
        stock = yf.Ticker(symbol)
        df = stock.history(period="10d", interval="30m")
        
        if df.empty:
            print(f"No data returned for {symbol}")
            continue

        df = df.reset_index()  # Ensure DateTime is a column

        for _, row in df.iterrows():
           
                        cursor.execute("""
            INSERT INTO dbo.HistoryStockData
            (Symbol, Price, DateTime, [Open], High, Low, [Close], Volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, symbol, row["Close"] , row["Datetime"], row["Open"], row["High"],
            row["Low"], row["Close"], row["Volume"])

    conn.commit()
    conn.close()

if __name__ == "__main__":
     while True:
        print(f"Fetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        fetch_and_store_halfhourly_data()
        print("Waiting for 60 seconds...\n")
        time.sleep(60)




