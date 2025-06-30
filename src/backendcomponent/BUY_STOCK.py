import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.fetchdata.sqlconnect import get_sql_connection

def buy_stock(user_id, symbol, quantity, price):
    conn = get_sql_connection()
    cursor = conn.cursor()
    total = quantity * price

    cursor.execute("SELECT initial_cash FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if not result or result[0] < total:
        return {"error": "Insufficient funds or user not found"}

    cursor.execute("SELECT quantity, avg_price FROM holding WHERE user_id = ? AND symbol = ?", (user_id, symbol))
    existing = cursor.fetchone()

    if existing:
        new_quantity = existing[0] + quantity
        new_avg = ((existing[0]*existing[1]) + (quantity*price)) / new_quantity
        cursor.execute("UPDATE holding SET quantity=?, avg_price=? WHERE user_id=? AND symbol=?",
                       (new_quantity, new_avg, user_id, symbol))
    else:
        cursor.execute("INSERT INTO holding (user_id, symbol, quantity, avg_price) VALUES (?, ?, ?, ?)",
                       (user_id, symbol, quantity, price))

    cursor.execute("UPDATE users SET initial_cash = initial_cash - ? WHERE id = ?", (total, user_id))
    cursor.execute("INSERT INTO transactions (user_id, symbol, quantity, price, type) VALUES (?, ?, ?, ?, 'buy')",
                   (user_id, symbol, quantity, price))

    conn.commit()
    return {"success": "Stock bought"}
