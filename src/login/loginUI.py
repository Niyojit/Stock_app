import streamlit as st
from login.logincomponent import register_user, authenticate_user
import datetime
import sys, os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.fetchdata.sqlconnect import get_sql_connection

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_mobile(mobile):
    return re.match(r'^\d{10}$', mobile)

def is_valid_password(password):
    return len(password) >= 6 and re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

def register(active_tab="Login"):
    st.set_page_config(page_title="Login | StockSphere", layout="centered")
    st.title("🔐 Welcome to StockSphere")
    
    query_params = st.query_params
    if "symbol" in query_params:
        st.experimental_set_query_params(symbol=query_params["symbol"])
   
    selected_tab = active_tab if "selected_tab" not in st.session_state else st.session_state.selected_tab
    selected_tab = st.radio("Choose an option:", ["Login", "Register"], index=0 if selected_tab == "Login" else 1)
    st.session_state.selected_tab = selected_tab

    if selected_tab == "Login":
        st.subheader("Login to your account")

        username_login = st.text_input("Username", key="login_username")
        password_login = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            auth_result = authenticate_user(username_login, password_login)
            if auth_result:
                st.session_state.username = auth_result["username"]
                st.session_state.user_id = auth_result["user_id"]
                st.success("✅ Login successful!")
                st.session_state.logged_in = True
               
                st.rerun()
            else:
                st.error("❌ Invalid username or password")


    elif selected_tab == "Register":
        st.subheader("Create a new account")

        username = st.text_input("👤 Register Username", key="register_username")
        email = st.text_input("📧 Email", key="email")
        mobile_no = st.text_input("📱 Mobile Number", key="mobile_no")

        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("🔒 Password", type="password", key="password")
        with col2:
            confirm_password = st.text_input("🔒 Confirm Password", type="password", key="confirm_password")

        dob = st.date_input("🎂 Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(), key="dob")
        gender = st.selectbox("⚧️ Gender", ("Male", "Female", "Other"), key="gender")

        if st.button("Register"):
            
            if not (username and password and confirm_password and email and mobile_no):
                st.warning("⚠️ Please fill all required fields.")
            elif password != confirm_password:
                st.error("🔁 Passwords do not match.")
            elif not is_valid_email(email):
                st.error("📧 Please enter a valid email address.")
            elif not is_valid_mobile(mobile_no):
                st.error("📱 Mobile number must be exactly 10 digits.")
            elif not is_valid_password(password):
                st.error("🔐 Password must be at least 6 characters and contain at least one special character.")
            else:
                
                success = register_user(username, password, email, mobile_no, dob, gender)
                if success:
                    st.success("🎉 Registration successful! You can now log in.")
                else:
                    st.error("❌ Registration failed. Username, email, or mobile may already exist.")
                   
        st.markdown("---")
    if st.button("← Back to Home"):
        st.session_state.show_auth = False
        st.rerun()



