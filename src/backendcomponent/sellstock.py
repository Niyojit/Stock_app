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

def show_sell_stock_details(symbol, username, user_id):
    conn = get_sql_connection()

    stock_df = pd.read_sql("SELECT * FROM dbo.IndianStockLiveData WHERE Symbol = ?", conn, params=[symbol])
    if stock_df.empty:
        st.warning("Stock data not found.")
        conn.close()
        return
    stock = stock_df.iloc[0]


    buy_df = pd.read_sql("""
        SELECT SUM(quantity) AS total_bought
        FROM dbo.StockBuyTransactions
        WHERE user_id = ? AND symbol = ?
    """, conn, params=[user_id, symbol])
    sell_df = pd.read_sql("""
        SELECT SUM(quantity) AS total_sold
        FROM dbo.StockSellTransactions
        WHERE user_id = ? AND symbol = ?
    """, conn, params=[user_id, symbol])

    total_bought = buy_df["total_bought"].iloc[0] or 0
    total_sold = sell_df["total_sold"].iloc[0] or 0
    net_quantity = total_bought - total_sold

    st.subheader(f"💸 Sell {stock['Name']} ({stock['Symbol']})")
    st.write(f"💼 You currently own: **{int(net_quantity)} shares**")

    if net_quantity <= 0:
        st.info("⚠ You haven't bought this stock yet or already sold all. Please purchase it first.")
        conn.close()
        return

    sell_qty = st.number_input("Quantity to Sell", min_value=1, max_value=int(net_quantity), step=1)
    sell_total = sell_qty * stock["Price"]
    st.info(f"Total Sale Amount: ₹{sell_total:.2f}")

    if st.button("Confirm Sale"):
        cur = conn.cursor()

        
        cur.execute("""
            IF OBJECT_ID('dbo.StockSellTransactions', 'U') IS NULL
                CREATE TABLE dbo.StockSellTransactions (
                    transaction_id UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
                    user_id INT,
                    username VARCHAR(100),
                    symbol NVARCHAR(20),
                    quantity INT,
                    price FLOAT,
                    total FLOAT,
                    time DATETIME DEFAULT GETDATE()
                )
            """)
      
        cur.execute("""
            INSERT INTO dbo.StockSellTransactions (user_id, username, symbol, quantity, price, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, symbol, sell_qty, stock["Price"], sell_total))

      
        cur.execute("UPDATE users SET Initial_cash = Initial_cash + ? WHERE id = ?", (sell_total, user_id))

        conn.commit()
        conn.close()
        st.success(f"✅ Sold {sell_qty} shares of {symbol} for ₹{sell_total:.2f}")
        st.session_state.sell_clicked = False
        st.rerun()