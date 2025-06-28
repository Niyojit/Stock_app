import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.fetchdata.sqlconnect import get_sql_connection



conn = get_sql_connection()
cursor = conn.cursor()

# USERS table
cursor.execute("""
IF OBJECT_ID('dbo.users', 'U') IS NULL
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(100) UNIQUE NOT NULL,
    password NVARCHAR(255) NOT NULL,
    initial_cash FLOAT DEFAULT 100000
);
""")

# HOLDING table
cursor.execute("""
IF OBJECT_ID('dbo.holding', 'U') IS NULL
CREATE TABLE holding (
    user_id INT NOT NULL,
    symbol NVARCHAR(20),
    quantity FLOAT,
    avg_price FLOAT,
    PRIMARY KEY(user_id, symbol),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
""")

# PRICE table
cursor.execute("""
IF OBJECT_ID('dbo.price', 'U') IS NULL
BEGIN
    CREATE TABLE price (
        id INT IDENTITY(1,1) PRIMARY KEY,
        ticketSymbol NVARCHAR(10),
        [date] DATETIME,
        [open] FLOAT,
        high FLOAT,
        low FLOAT,
        [close] FLOAT,
        volume BIGINT
    )
END
""")


# TRANSACTIONS table
cursor.execute("""
IF OBJECT_ID('dbo.transactions', 'U') IS NULL
CREATE TABLE transactions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    symbol NVARCHAR(20),
    quantity FLOAT,
    price FLOAT,
    type NVARCHAR(10),
    date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
""")

class StockMarket:
    def __init__(self):
        self.conn = get_sql_connection()
        self.cursor = self.conn.cursor()
    

    def add_cash(self, user_id, amount):
        try:
            self.cursor.execute("select initial_cash from users where id = ?", (user_id,))
            initial_amount = self.cursor.fetchone()

            if not initial_amount:
                return {"error" : "User not found "}
            elif initial_amount[0] < 0:
                return {"error":"insufficient funds"}
            
            self.cursor.execute("update users set initial_cash = initial_cash + ? where id = ?", (amount, user_id))
            self.conn.commit()

            return {"success": "Cash added successfull"}
            
        except Exception as e:
            return {"error": str(e)}

                
            
    def buy_stock(self, user_id, symbol, quantity, price):
        try:
            cost = quantity * price


            self.cursor.execute("SELECT initial_cash FROM users WHERE id = ?", (user_id,))
            result1 = self.cursor.fetchone()

            if not result1:
                return {"error":"User Not Found"}

            elif result1[0] < cost:
                return {"error": "Insufficient funds"}
            

            self.cursor.execute("select avg_price, quantity from holding where user_id = ? and symbol = ?", (user_id, symbol))
            existing_holding = self.cursor.fetchone()

            if existing_holding:
                old_avg_price, old_quantity = existing_holding
                new_quantity = old_quantity + quantity
                new_avg = ((old_quantity * old_avg_price) + (quantity * price)) / new_quantity

                self.cursor.execute("update holding set quantity = ?, avg_price =? where user_id = ? and symbol = ?",(new_quantity, new_avg, user_id, symbol))

            else:
                self.cursor.execute("Insert into holding (user_id, symbol, quantity, avg_price) values (?, ?, ?, ?)",(user_id, symbol, quantity, price))

            self.cursor.execute("UPDATE users SET initial_cash = initial_cash - ? WHERE id = ?", (cost, user_id))

            self.cursor.execute("INSERT INTO transactions (user_id, symbol, quantity, price, type) VALUES (?, ?, ?, ?, 'buy')",
                        (user_id, symbol, quantity, price))

            self.conn.commit()
            return {"success": "Stock bought"}

        except Exception as e:
            return {"error": str(e)}
    
    def sell_stock(self,user_id, symbol, quantity, price):
        try:
            self.cursor.execute("select quantity from holding where user_id = ? and symbol = ?", (user_id, symbol))
            existing_holding = self.cursor.fetchone()

            if not existing_holding:
                return {"error":"No holdings"}
            elif existing_holding[0] < quantity:
                return {"error": "Insufficient quantity to sell"}
            
            total_value = quantity*price

            self.cursor.execute("update holding set quantity = quantity - ? where user_id = ? and symbol = ?", (quantity, user_id, symbol))

            self.cursor.execute("update users set initial_cash = initial_cash + ? where id = ?", (total_value, user_id))

            self.cursor.execute("Insert into transactions (user_id, symbol, quantity, price, type) values(?, ?, ?,?, 'sell')",
                           (user_id, symbol, quantity,price))
            

            self.conn.commit()
            return {"success": "Stock sold"}

            
        except Exception as e:
            return {"error": str(e)}        

    def get_portfolio(self, user_id):
        try:
            self.cursor.execute("select h.symbol, h.quantity, h.avg_price from holding where user_id = ?", (user_id,) )
            my_holdings = self.cursor.fetchall()

            if not my_holdings:
                return{"error": "No holdings for this User"}
            
            return {"Portfolio": my_holdings}
        
        except Exception as e:
            return {"error": str(e)}
        
    def get_transactions(self, user_id):
        try:
            self.cursor.execute("select t.symbol, t.quantity, t.price, t.type, t.date from transactions where user_id = ?",(user_id,))
            my_transactons = self.cursor.fetchall()

            if not my_transactons:
                return {"error": "No transactions made by this User"}
            
            return {"Transactions" : my_transactons}
            
        except Exception as e:
            return {"error": str(e)}
        

# conn.commit()
# testing 
# Insert or get user ID
# username = "Abhay"
# cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
# user = cursor.fetchone()

# if user:
#     user_id = user[0]
#     print("User already exists with ID:", user_id)
# else:
#     cursor.execute("""
#     INSERT INTO users (username, password, initial_cash)
#     VALUES (?, ?, ?)
#     """, ("Abhay", "1234", 100000))
#     conn.commit()
#     cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
#     user_id = cursor.fetchone()[0]
#     print("New user created with ID:", user_id)

# # # Buy stock
# sm = StockMarket()
# result = sm.buy_stock(user_id=user_id, symbol="LIC", quantity=1000, price=100)
# print("Buy result:", result)

# # Sell stock
# # result = sm.sell_stock(user_id=user_id, symbol="LIC", quantity=50, price=10)
# # print("Sell result:", result)

# if result.get("error", "").lower() == "insufficient funds":
#     print("Insufficient funds to buy stock.")
#     choice = input("Do you want to add cash? (yes/No): ").strip().lower()

#     if choice == "yes":
#         try:
#             amount = float(input("Enter the amount you want to add: "))
#             add_cash_result = sm.add_cash(user_id =user_id, amount = amount)
#             print("Csh added successfully:", add_cash_result)
#             result = sm.buy_stock(user_id = user_id, symbol = "LIC", quantity= 1000, price = 100)
#         except ValueError:
#             print("Invalid Amount entered. Please enter a valid number.")
# print("Buy result:", result)



# To delete all the data

cursor.execute("DELETE FROM transactions")
cursor.execute("DELETE FROM holding")
cursor.execute("DELETE FROM price")
cursor.execute("DELETE FROM users")
conn.commit()
print("All data deleted.")




# if __name__ =="__main__":
#     stock_market = StockMarket()

# print(stock_market.buy_stock(1,'AAPL',10,150))