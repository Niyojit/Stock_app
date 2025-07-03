import streamlit as st
import pandas as pd
import os
import sys
from streamlit_autorefresh import st_autorefresh

# ✅ Path setup for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection


# 🔥 Fetch user holdings with live price integration
def get_user_holdings(user_id):
    conn = get_sql_connection()

    # 🛒 Total Buy Summary
    buy_df = pd.read_sql("""
        SELECT symbol, SUM(quantity) AS bought_qty, AVG(price) AS avg_price, SUM(total) AS total_buy
        FROM dbo.StockBuyTransactions
        WHERE user_id = ?
        GROUP BY symbol
    """, conn, params=[user_id])

    if buy_df.empty:
        conn.close()
        return pd.DataFrame()

    # 🏷️ Total Sell Summary
    sell_df = pd.read_sql("""
        SELECT symbol, SUM(quantity) AS sold_qty
        FROM dbo.StockSellTransactions
        WHERE user_id = ?
        GROUP BY symbol
    """, conn, params=[user_id])

    # 🔗 Merge Buy & Sell
    df = pd.merge(buy_df, sell_df, on="symbol", how="left")
    df["sold_qty"] = df["sold_qty"].fillna(0)
    df["net_qty"] = df["bought_qty"] - df["sold_qty"]

    # ➕ Filter stocks still held
    df = df[df["net_qty"] > 0]

    # 🔄 Standardize symbols (Ensure ".NS" suffix for matching live data)
    df["symbol"] = df["symbol"].apply(lambda x: x if x.endswith('.NS') else x + '.NS')

    # 🔥 Fetch Latest Stock Prices for each symbol
    live_prices = pd.read_sql("""
        SELECT l.Symbol, l.Price AS current_price
        FROM dbo.IndianStockLiveData l
        INNER JOIN (
            SELECT Symbol, MAX(FetchTime) AS LatestFetch
            FROM dbo.IndianStockLiveData
            GROUP BY Symbol
        ) m ON l.Symbol = m.Symbol AND l.FetchTime = m.LatestFetch
    """, conn)

    conn.close()

    # 🔗 Merge live prices
    df = df.merge(live_prices, left_on="symbol", right_on="Symbol", how="left")

    # 💰 Calculations
    df["current_value"] = df["net_qty"] * df["current_price"]
    df["investment"] = df["net_qty"] * df["avg_price"]
    df["gain_loss"] = df["current_value"] - df["investment"]

    return df


# 🎯 Streamlit Page to Display Holdings
def holding_page(username, user_id):
    st.title("📦 My Holdings")
    st_autorefresh(interval=3000, key="refresh_explore", limit=None)
    if not st.session_state.get("logged_in"):
        st.error("⚠️ You must be logged in to view holdings.")
        return

    df = get_user_holdings(user_id)

    if df.empty:
        st.info("📭 You don't currently hold any stocks.")
        return

    st.markdown(f"### 👤 Holdings for **{username}**")

    df_display = df[[ 
        "symbol", "net_qty", "avg_price", "current_price", "investment", "current_value", "gain_loss"
    ]].copy()

    df_display.rename(columns={
        "symbol": "Stock Symbol",
        "net_qty": "Quantity",
        "avg_price": "Avg Buy Price (₹)",
        "current_price": "Current Price (₹)",
        "investment": "Investment (₹)",
        "current_value": "Current Value (₹)",
        "gain_loss": "Gain/Loss (₹)"
    }, inplace=True)

    # ✅ Apply currency formatting
    for col in ["Avg Buy Price (₹)", "Current Price (₹)", "Investment (₹)", "Current Value (₹)", "Gain/Loss (₹)"]:
        df_display[col] = df_display[col].apply(lambda x: f"₹{x:,.2f}")

    st.dataframe(df_display, use_container_width=True)
 
 