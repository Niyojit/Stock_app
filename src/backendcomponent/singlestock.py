import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection

def show_stock_details():
    query_params = st.query_params
    symbol = query_params.get("symbol")

    if not symbol:
        st.error("No stock selected.")
        return

    conn = get_sql_connection()
    df = pd.read_sql(f"SELECT * FROM dbo.IndianStockLiveData WHERE Symbol = '{symbol}'", conn)
    conn.close()

    if df.empty:
        st.warning("Stock not found.")
        return

    stock = df.iloc[0]
    st.title(f"{stock['Name']} ({stock['Symbol']})")
    st.write(f"**Price:** ₹{stock['Price']}")
    st.write(f"**P/E Ratio:** {stock['PERatio']}")
    st.write(f"**52W High:** ₹{stock['High52W']}")
    st.write(f"**52W Low:** ₹{stock['Low52W']}")
    st.write(f"**Sector:** {stock['Sector']}")


    if "buy_clicked" not in st.session_state:
        st.session_state.buy_clicked = False
    if "confirm_clicked" not in st.session_state:
        st.session_state.confirm_clicked = False

    if st.button("🛒 Buy Stock"):
        st.session_state.buy_clicked = True
        st.session_state.confirm_clicked = False  # Reset confirmation

    if st.session_state.buy_clicked:
        quantity = st.number_input("Enter quantity", min_value=1, step=1, key="buy_quantity")
        if st.button("Confirm Purchase"):
            st.session_state.confirm_clicked = True

        if st.session_state.confirm_clicked:
            total_cost = stock['Price'] * st.session_state.buy_quantity
            st.success(f"✅ Purchased {st.session_state.buy_quantity} shares of {stock['Name']} for ₹{total_cost:.2f}")
            st.write(f"Your total amount is {total_cost} and you have only 500rs")
    
    if st.button("🔙 Back to Explore"):
        st.session_state.buy_clicked = False
        st.session_state.confirm_clicked = False
        st.query_params.clear()
        st.rerun()

