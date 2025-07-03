import yagmail
import pandas as pd
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetchdata.sqlconnect import get_sql_connection

# Connect to database
conn = get_sql_connection()

# Fetch user details
users_df = pd.read_sql("SELECT id, username, email FROM users", conn)

# Get latest prices
latest_prices = pd.read_sql("""
    SELECT Symbol, Price AS current_price
    FROM dbo.IndianStockLiveData
    WHERE FetchTime = (SELECT MAX(FetchTime) FROM dbo.IndianStockLiveData)
""", conn)

# Email credentials
sender_email = "abhaydhuriya860@gmail.com"
app_password = "ukcwarbtivmagael"
yag = yagmail.SMTP(user=sender_email, password=app_password)

# Loop through users
for _, user in users_df.iterrows():
    user_id = user["id"]
    username = user["username"]
    email = user["email"]

    # ✅ Skip if email is missing or invalid
    if not isinstance(email, str) or "@" not in email:
        print(f"⛔ Skipped: Invalid or missing email for {username}")
        continue

    # Holdings
    buy_df = pd.read_sql("""
        SELECT symbol, SUM(quantity) AS bought_qty, AVG(price) AS avg_price
        FROM dbo.StockBuyTransactions
        WHERE user_id = ?
        GROUP BY symbol
    """, conn, params=[user_id])

    sell_df = pd.read_sql("""
        SELECT symbol, SUM(quantity) AS sold_qty
        FROM dbo.StockSellTransactions
        WHERE user_id = ?
        GROUP BY symbol
    """, conn, params=[user_id])

    holdings = pd.merge(buy_df, sell_df, on="symbol", how="left")
    holdings["sold_qty"] = holdings["sold_qty"].fillna(0)
    holdings["net_qty"] = holdings["bought_qty"] - holdings["sold_qty"]
    holdings = holdings[holdings["net_qty"] > 0]
    holdings = holdings.merge(latest_prices, left_on="symbol", right_on="Symbol", how="left")

    if holdings.empty:
        continue

    lines = []
    for _, row in holdings.iterrows():
        lines.append(f"📈 {row['symbol']}: {int(row['net_qty'])} shares @ ₹{row['current_price']:.2f}")

    body = "\n".join(lines)
    today = datetime.now().strftime("%d %B %Y")
    subject = f"📬 Daily Holdings Report - {today}"

    content = f"""
Hello {username},

Here is your daily stock holding summary:

{body}

Regards,
Abhay Dhuriya Limited Team
"""

    try:
        yag.send(to=email, subject=subject, contents=content)
        print(f"✅ Sent to {username} ({email})")
    except Exception as e:
        print(f"❌ Failed for {email}: {e}")

conn.close()
