import streamlit as st
import pandas as pd
import os
import sys
from streamlit_autorefresh import st_autorefresh
from urllib.parse import urlencode

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection
from fetchdata.api import fetch_and_store_stocks

# Fetch live stock data
def fetch_live_stock_data(limit=20):
    conn = get_sql_connection()
    query = f"""
        SELECT TOP {limit}
            Symbol,
            Name,
            Price,
            PERatio,
            High52W,
            Low52W,
            Sector
        FROM dbo.IndianStockLiveData
        ORDER BY FetchTime DESC 
    """
    df = pd.read_sql(query, conn)
    conn.close()

    stocks = []
    for _, row in df.iterrows():
        price = round(row.Price, 2)
        change_pct = ((row.Price - row.Low52W) / (row.High52W - row.Low52W + 0.01)) * 100
        change_color = "green" if change_pct > 50 else "red"
        stocks.append({
            "name": row.Name,
            "price": f"₹{price}",
            "symbol": row.Symbol,
            "change_pct": f"{change_pct:.2f}%",
            "color": change_color
        })
    return stocks

def explorepage():
    
    fetch_and_store_stocks()

    stocks = fetch_live_stock_data()
    st.title("📈 Explore Stocks")

    for stock in stocks:
        query_str = urlencode({"symbol": stock["symbol"]})
        url = f"?{query_str}"
        st.markdown(
            f"""
            <div style='margin-bottom:10px;'>
                <a href="{url}" style='text-decoration:none; color: black;'>
                    <b>{stock['name']}</b> &nbsp;&nbsp;|&nbsp;&nbsp;
                    Price: {stock['price']} &nbsp;&nbsp;|&nbsp;&nbsp;
                    <span style='color:{stock['color']};'>Change: {stock['change_pct']}</span>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

