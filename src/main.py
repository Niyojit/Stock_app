import pyodbc

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DREAM;'
    'DATABASE=stockdata;'
    'UID=sa;'
    'PWD=training@123'
)


conn = pyodbc.connect("".join(conn))

conn_str= conn.cursor()

conn_str.execute("select * from products;").fetchall()

