import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import bcrypt
from src.fetchdata.sqlconnect import get_sql_connection

def authenticate_user(username, password):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode(), result[0].encode()):
        return True
    return False
