import streamlit as st
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.fetchdata.sqlconnect import get_sql_connection

def fetch_balance( user_id):

    


    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Initial_cash FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    balance = result[0] if result else 0.0
    cursor.close()
    conn.close()
    return balance

def my_money(username, user_id):
    username = username or st.session_state.get("username", "")
    user_id = user_id or st.session_state.get("user_id", None)
    st.session_state.logged_in = True
    balance = fetch_balance( user_id)

    col1, col2 = st.columns([2, 1.5])
    with col1:
        st.markdown("<h4>Wallet Balance</h4>", unsafe_allow_html=True)
        with st.expander("My Wallet", expanded=True):
            st.markdown("### Total Balance")
            st.metric(label="Stock Balance", value=f"₹{balance:,.2f}")
        

    with col2:
        st.markdown("<h4>Bank Transactions</h4>", unsafe_allow_html=True)
        with st.expander("Bank Actions", expanded=True):
            tab1, tab2 = st.tabs(["Add money", "Withdraw"])

            with tab1:
                col3, col4 = st.columns([1, 1])
                with col3:
                    st.write("Enter amount to add to wallet:")
                with col4:
                    add_amt = st.number_input(
                        "Add money", min_value=0.0, step=100.0, key="add_money_input",
                        label_visibility="collapsed", placeholder="Enter amount"
                    )

                if st.button("Add Money", use_container_width=True, key="add_btn"):
                    if add_amt <= 0:
                        st.warning("⚠️ Enter a positive amount.")
                    else:
                        new_balance = balance + add_amt
                        conn = get_sql_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE users SET Initial_cash = ? WHERE id = ?",
                            (new_balance, user_id)
                        )
                        log_transaction(user_id, username, add_amt, "Deposited")
                        conn.commit()
                        cursor.close()
                        conn.close()

                        st.success(f"✅ ₹{add_amt} added to wallet.")
                        st.session_state["wallet_updated"] = True
                        st.rerun()
                        

            with tab2:
                col5, col6 = st.columns([1, 1])
                with col5:
                    st.write("Enter amount to withdraw from wallet:")
                with col6:
                    withdraw_amt = st.number_input(
                        "Withdraw money", min_value=0.0, step=100.0, key="withdraw_money_input",
                        label_visibility="collapsed", placeholder="Enter amount"
                    )

                if st.button("Withdraw Money", use_container_width=True, key="withdraw_btn"):
                    if withdraw_amt <= 0:
                        st.warning("⚠️ Enter a positive amount.")
                    elif withdraw_amt > balance:
                        st.error("❌ Insufficient balance.")
                    else:
                        new_balance = balance - withdraw_amt
                        conn = get_sql_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE users SET Initial_cash = ? WHERE id = ?",
                            (new_balance, user_id)
                        )
                     
                        log_transaction(user_id, username, withdraw_amt, "Withdrawn")
                       
                        conn.commit()
                        cursor.close()
                        conn.close()

                        st.success(f"✅ ₹{withdraw_amt} withdrawn from wallet.")
                        st.session_state["wallet_updated"] = True
                        st.rerun()
                        

def log_transaction(user_id, username, amount, status):
    if not username:
        st.error("Session expired. Please log in again.")
        return

    conn = get_sql_connection()
    cursor = conn.cursor()

    transaction_id = str(uuid.uuid4())[:8]  

  
    cursor.execute("""
        INSERT INTO MoneyTransactionHistory (Money_Transaction_id, user_id, username, Amount, Status)
        VALUES (?, ?, ?, ?, ?)
    """, (transaction_id, user_id, username, amount, status))
    st.success("Amount added successfully!")
    
    conn.commit()
    
    cursor.close()
    conn.close()
