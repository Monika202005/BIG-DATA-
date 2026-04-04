import mysql.connector
from mysql.connector import Error

OLTP_CONFIG = {
    'host': 'localhost',
    'user': 'ecommerce_user',
    'password': 'Ecommerce_pass123!',
    'database': 'ecommerce_oltp'
}

DW_CONFIG = {
    'host': 'localhost',
    'user': 'ecommerce_user',
    'password': 'Ecommerce_pass123!',
    'database': 'ecommerce_dw'
}

def get_oltp_connection():
    try:
        conn = mysql.connector.connect(**OLTP_CONFIG)
        if conn.is_connected():
            print("✅ Connected to ecommerce_oltp")
            return conn
    except Error as e:
        print(f"❌ OLTP Connection failed: {e}")
        return None

def get_dw_connection():
    try:
        conn = mysql.connector.connect(**DW_CONFIG)
        if conn.is_connected():
            print("✅ Connected to ecommerce_dw")
            return conn
    except Error as e:
        print(f"❌ DW Connection failed: {e}")
        return None
