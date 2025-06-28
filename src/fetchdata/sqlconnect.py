import pyodbc
import pandas as pd

def get_sql_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-8AVP1A3;"  
            "DATABASE=stockdata;"   
            "Trusted_Connection=yes;"
        )

        print("Connected to SQL Server successfully.")
        return conn
    except pyodbc.Error as e:
        print("Error connecting to SQL Server:", e)
        return None
    
    



