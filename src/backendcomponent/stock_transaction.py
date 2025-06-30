import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.fetchdata.sqlconnect import get_sql_connection

def get_transactions(user_id):
    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT symbol, quantity, price, type, date FROM transactions WHERE user_id = ?", (user_id,))
        transactions = cursor.fetchall()
        if not transactions:
            return {"message": "No transactions"}
        return {"transactions": transactions}
    except Exception as e:
        return {"error": str(e)}
