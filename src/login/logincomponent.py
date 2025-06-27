import sys
import os
import bcrypt
import streamlit as st
import datetime
#streamlit run "d:\Bootcamp june 2025\stocks_app\Stock_app\src\login\logincomponent.py"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.fetchdata.sqlconnect import get_sql_connection

conn = get_sql_connection()
cursor = conn.cursor()

# ✅ Create users table (if not exists)
cursor.execute("""
IF OBJECT_ID('dbo.users', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.users (
        [id] INT PRIMARY KEY IDENTITY(1,1),
        [username] NVARCHAR(50) UNIQUE,
        [password_hash] NVARCHAR(255),
        [email] NVARCHAR(100) UNIQUE,
        [Mobile_no] NVARCHAR(15) UNIQUE,
        [DOB] DATE,
        [Gender] VARCHAR(10)
    )
END
""")
conn.commit()

# ✅ Register function
def register_user(username, password, email, mobile_no, dob, gender):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    dob_str = dob.strftime('%Y-%m-%d') 
    try:
        cursor.execute("INSERT INTO users (username, password_hash, email, Mobile_no, DOB, Gender) VALUES (?, ?, ?, ?, ?, ?)", (username, hashed, email, mobile_no, dob_str, gender))
        conn.commit()
        return True
    except Exception as e:
        print("Registration failed:", e)
        return False

# ✅ Authenticate function
def authenticate_user(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        stored_hash = result[0]
        return bcrypt.checkpw(password.encode(), stored_hash.encode())
    return False

import streamlit as st

st.title("Welcome to the Stock App")

# Ask the user if they're registered
auth_mode = st.selectbox("Select Mode", ["Login", "Register"])


# Get user input
username = st.text_input("Username", key="username")
password = st.text_input("Password", type="password", key="password")

if auth_mode == "Login":
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid username or password")

elif auth_mode == "Register":
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    email = st.text_input("Email", key="email")
    mobile_no = st.text_input("Mobile Number", key="mobile_no")
    dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today(), key="dob")
    gender = st.selectbox("Gender", ("Male", "Female", "Other"), key="gender")


    if st.button("Register"):
        if not (username and password and confirm_password and email and mobile_no):
            st.error("Please fill all required fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            # You can extend register_user() to accept these fields
            if register_user(username, password, email, mobile_no, dob, gender):
                st.success("Registration successful! Please log in.")
                for key in ["username", "password", "confirm_password", "email", "mobile_no", "dob", "gender"]:
                    if key in st.session_state:
                        del st.session_state[key]
            else:
                st.error("Registration failed. Username may already exist.")
# ✅ Display registered users (for debugging purposes)