import streamlit as st
from .logincomponent import register_user, authenticate_user
import datetime

def register(active_tab="Login"):
    st.set_page_config(page_title="Login | StockSphere", layout="centered")
    st.title("🔐 Welcome to StockSphere")

    # Use radio buttons to simulate tab switching
    selected_tab = active_tab if "selected_tab" not in st.session_state else st.session_state.selected_tab
    selected_tab = st.radio("Choose an option:", ["Login", "Register"], index=0 if selected_tab == "Login" else 1)
    st.session_state.selected_tab = selected_tab

    if selected_tab == "Login":
        st.subheader("Login to your account")

        username_login = st.text_input("Username", key="login_username")
        password_login = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if authenticate_user(username_login, password_login):
                st.success("✅ Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = username_login
            else:
                st.error("❌ Invalid username or password")

    elif selected_tab == "Register":
        st.subheader("Create a new account")

        username = st.text_input("👤 Username", key="username")
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
            else:
                if register_user(username, password, email, mobile_no, dob, gender):
                    st.success("🎉 Registration successful! You can now log in.")
                else:
                    st.error("❌ Registration failed. Username or Email may already exist.")
                    
        st.markdown("---")
    if st.button("← Back to Home"):
        st.session_state.show_auth = False
        st.rerun()
