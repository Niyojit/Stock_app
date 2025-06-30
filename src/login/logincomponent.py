import sys
import os
import bcrypt
#streamlit run "d:\Bootcamp june 2025\stocks_app\src\login\logincomponent.py"
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

