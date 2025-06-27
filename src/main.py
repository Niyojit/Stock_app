import pyodbc

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-8AVP1A3;'
    'DATABASE=stockdata;'
    'UID=sa;'
    'PWD=training@123'
)


conn = pyodbc.connect("".join(conn))

conn_str= conn.cursor()

conn_str.execute("select * from products;").fetchall()

