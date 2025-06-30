import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.fetchdata.sqlconnect import get_sql_connection

def add_cash(user_id, amount):
    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT initial_cash FROM users WHERE id = ?", (user_id,))
    if (row := cursor.fetchone()) is None:
        return {"error": "User not found"}

    cursor.execute("UPDATE users SET initial_cash = initial_cash + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    return {"success": f"Added ₹{amount}"}
