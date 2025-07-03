import streamlit as st
from backendcomponent.wallet import my_money
import sys
import os
import pandas as pd
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.fetchdata.sqlconnect import get_sql_connection



def money_transaction(username, user_id):
    st.set_page_config(page_title="Money Transaction", layout="wide", initial_sidebar_state="expanded")
    

    

   
    username = username or st.session_state.get("username", "")
    user_id = user_id or st.session_state.get("user_id", None)

    if not username or user_id is None:
        st.error("⚠️ Session expired. Please log in again.")
        return


    if st.session_state.get("wallet_updated", False):
        st.session_state["wallet_updated"] = False
        
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF OBJECT_ID('dbo.MoneyTransactionHistory', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo.MoneyTransactionHistory (
                Money_Transaction_id VARCHAR(50) PRIMARY KEY,
                user_id INT,
                username VARCHAR(100),
                Amount FLOAT,
                Status VARCHAR(200),
                time DATETIME DEFAULT GETDATE()
            )
        END
        """)
    conn.commit()

    # ✅ Read Amount (not Money) to match insert
    cursor.execute("""
    SELECT Money_Transaction_id, username, Amount, time, Status FROM MoneyTransactionHistory WHERE user_id = ?""", (user_id,))
    fetched = cursor.fetchall()
    # ✅ Force-unpack all rows
    records = [r[0] if len(r) == 1 and isinstance(r[0], tuple) else r for r in fetched]


    valid_records = [r for r in records if len(r) == 5]

    if not valid_records:
        st.info("No transactions found.")
        return
    
    st.markdown(f"### 💰 Transaction History")

    for trx in valid_records:
        # ✅ Force unpack inner tuple if needed
        if len(trx) == 1 and isinstance(trx[0], tuple):
            trx = trx[0]

        if len(trx) != 5:
            continue  # Skip malformed rows

        trx_id, username, amount, time, status = trx

        if isinstance(time, str):
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")

        with st.expander(f"🗓️ Transaction Date: {time.strftime('%d %b %Y, %I:%M %p')}"):
            st.write(f"**Transaction ID:** {trx_id}")
            st.write(f"**Username:** {username}")
            st.write(f"**Amount:** ₹{amount:,.2f}")
            if status == "Deposited":
                st.markdown(f"**Status:** 🟢 <span style='color:green'>{status}</span>", unsafe_allow_html=True)
            elif status == "Withdrawn":
                st.markdown(f"**Status:** 🔴 <span style='color:red'>{status}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**Status:** {status}")
        


    conn.commit()
    cursor.close()
    conn.close()
   
























   