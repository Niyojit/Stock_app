import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.fetchdata.sqlconnect import get_sql_connection

conn = get_sql_connection()
cursor = conn.cursor()

cursor.execute("select Initial_cash from users where id = ? ",(id))
value = cursor.fetchone()

def my_money():
    col1, col2 = st.columns([2, 1.5])
    with col1:
        st.markdown("<h4>Wallet Balance</h4>", unsafe_allow_html=True)
        
        with st.expander("My Wallet", expanded = True):
                    st.markdown("### Total Balance")
                    st.metric(label="Stock Balance", value=f"{value}", delta="₹500 (5%)")

        st.button("All Transactions", use_container_width=True)

    with col2:
        st.markdown("<h4>Wallet Balance</h4>", unsafe_allow_html=True)
        
        with st.expander("Bank Transactions", expanded = True):
                tab1, tab2 = st.tabs(["Add money", "Withdraw"]) 
                with tab1:
                    col3, col4 = st.columns([1,1])
                    with col3:
                        st.write("Enter amount to add to wallet:")
                    with col4:
                        st.text_input("Add money", label_visibility="collapsed", placeholder="Enter amount", key="add_money")
                    st.button("Add Money", use_container_width=True)
                with tab2:
                    col3, col4 = st.columns([1,1])
                    with col3:
                        st.write("Enter amount to withdraw from wallet:")
                    with col4:
                        st.text_input("Add money", label_visibility="collapsed", placeholder="Enter amount", key="withdraw_money")
                    st.button("Withdraw Money", use_container_width=True)