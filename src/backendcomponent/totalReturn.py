import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.fetchdata.sqlconnect import get_sql_connection

def get_total_returns(user_id):
    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT symbol, quantity, avg_price FROM holding WHERE user_id = ?", (user_id,))
        holdings = cursor.fetchall()
        total_invested = 0
        current_value = 0

        for symbol, quantity, avg_price in holdings:
            total_invested += quantity * avg_price
            cursor.execute(
                "SELECT TOP 1 [close] FROM price WHERE ticketSymbol = ? ORDER BY [date] DESC",
                (symbol,)
            )
            latest_price = cursor.fetchone()
            if latest_price:
                current_value += quantity * latest_price[0]

        total_returns = current_value - total_invested
        return {"total_returns": round(total_returns, 2)}
    except Exception as e:
        return {"error": str(e)}
