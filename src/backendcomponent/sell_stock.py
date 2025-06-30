import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.fetchdata.sqlconnect import get_sql_connection

def sell_stock(user_id, symbol, quantity, price):
    conn = get_sql_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT quantity FROM holding WHERE user_id = ? AND symbol = ?", (user_id, symbol))
        holding = cursor.fetchone()

        if not holding:
            return {"error": "No holdings found for this stock."}
        elif holding[0] < quantity:
            return {"error": "Not enough quantity to sell."}

        total = quantity * price
        cursor.execute("UPDATE holding SET quantity = quantity - ? WHERE user_id = ? AND symbol = ?", (quantity, user_id, symbol))
        cursor.execute("UPDATE users SET initial_cash = initial_cash + ? WHERE id = ?", (total, user_id))
        cursor.execute("INSERT INTO transactions (user_id, symbol, quantity, price, type) VALUES (?, ?, ?, ?, 'sell')",
                       (user_id, symbol, quantity, price))

        conn.commit()
        return {"success": "Stock sold."}

    except Exception as e:
        return {"error": str(e)}
