import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.fetchdata.sqlconnect import get_sql_connection

def get_current_investment_value(user_id):
    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT symbol, quantity FROM holding WHERE user_id = ?", (user_id,))
        holdings = cursor.fetchall()
        current_value = 0
        for symbol, quantity in holdings:
            cursor.execute(
                "SELECT TOP 1 [close] FROM price WHERE ticketSymbol = ? ORDER BY [date] DESC",
                (symbol,)
            )
            latest_price = cursor.fetchone()
            if latest_price:
                current_value += quantity * latest_price[0]
        return {"current_value": round(current_value, 2)}
    except Exception as e:
        return {"error": str(e)}
