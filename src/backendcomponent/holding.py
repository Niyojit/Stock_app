import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.fetchdata.sqlconnect import get_sql_connection

def get_portfolio(user_id):
    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT symbol, quantity, avg_price FROM holding WHERE user_id = ?", (user_id,))
        holdings = cursor.fetchall()
        if not holdings:
            return {"message": "No holdings"}
        return {"portfolio": holdings}
    except Exception as e:
        return {"error": str(e)}
