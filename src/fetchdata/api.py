# stock_fetcher.py

import yfinance as yf
import pandas as pd
from fetchdata.sqlconnect import get_sql_connection

import os
import sys


# Set up backend path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
top_20_symbols = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "AXISBANK.NS", "LT.NS", "ITC.NS", "HINDUNILVR.NS",
    "BHARTIARTL.NS", "ASIANPAINT.NS", "BAJFINANCE.NS", "KOTAKBANK.NS",
    "MARUTI.NS", "HCLTECH.NS", "SUNPHARMA.NS", "WIPRO.NS", "POWERGRID.NS", "NTPC.NS"
]

def fetch_and_store_stocks():
    conn = get_sql_connection()
    cursor = conn.cursor()

    # Create table if not exists
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

    stocks = yf.Tickers(" ".join(top_20_symbols))
    for symbol in top_20_symbols:
        info = stocks.tickers[symbol].info
        row = {
            "Symbol": symbol,
            "Name": info.get("longName", ""),
            "Price": info.get("regularMarketPrice", None),
            "MarketCap": info.get("marketCap", None),
            "PERatio": info.get("trailingPE", None),
            "High52W": info.get("fiftyTwoWeekHigh", None),
            "Low52W": info.get("fiftyTwoWeekLow", None),
            "Volume": info.get("volume", None),
            "Sector": info.get("sector", "")
        }
        cursor.execute("""
            INSERT INTO dbo.IndianStockLiveData
            (Symbol, Name, Price, MarketCap, PERatio, High52W, Low52W, Volume, Sector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row["Symbol"], row["Name"], row["Price"], row["MarketCap"],
            row["PERatio"], row["High52W"], row["Low52W"], row["Volume"], row["Sector"])
    conn.commit()
    conn.close()
