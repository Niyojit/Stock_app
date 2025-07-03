import streamlit as st
import pandas as pd
import os
import sys
from urllib.parse import urlencode
import uuid
from streamlit_autorefresh import st_autorefresh


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection
from fetchdata.api import fetch_and_store_stocks
from backendcomponent.sellstock import show_sell_stock_details
from backendcomponent.buystock import show_selected_stock_details

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


def explorepage(username, user_id):
     
    if not st.session_state.get("selected_symbol"):
        st_autorefresh(interval=60000, key="refresh_explore")
    
    stocks = fetch_live_stock_data()
    st.title("📈 Explore Stocks")

    search_input = st.text_input("🔍 Search for stocks by symbol or name")

    if search_input:
        stocks = [s for s in stocks if search_input.lower() in s['symbol'].lower() or search_input.lower() in s['name'].lower()]

        if not stocks:
            st.warning("❌ No matching stocks found.")
            return

    for idx, stock in enumerate(stocks):
        unique_key = f"{stock['symbol']}_{idx}"
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f"{stock['name']} | ₹{stock['price']} | "
                f":{'🟢:' if stock['color'] == 'green' else 'red_circle:'} {stock['change_pct']}"
            )
        with col2:
            if st.button("View", key=unique_key):
                st.session_state.selected_symbol = stock["symbol"]
                st.session_state.buy_clicked = False
                st.session_state.sell_clicked = False
                st.session_state.confirm_clicked = False
                st.rerun()

                
    if st.session_state.get("selected_symbol"):
        show_selected_stock_details(st.session_state.selected_symbol, username, user_id)












