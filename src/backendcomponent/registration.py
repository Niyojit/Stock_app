
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import bcrypt
from src.fetchdata.sqlconnect import get_sql_connection


def register_user(username, password, email, mobile_no, dob, gender):
    conn = get_sql_connection()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, Mobile_no, DOB, Gender) VALUES (?, ?, ?, ?, ?, ?)",
            (username, hashed, email, mobile_no, dob, gender)
        )
        conn.commit()
        return {"success": "User registered"}
    except Exception as e:
        return {"error": str(e)}
