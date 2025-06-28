import pyodbc

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-HSG1FD5R;'
    'DATABASE=stockdata;'
    'UID=sa;'
    'PWD=training@123'
)


conn = pyodbc.connect("".join(conn))

conn_str= conn.cursor()

conn_str.execute("select * from products;").fetchall()

