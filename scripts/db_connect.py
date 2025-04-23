import sqlite3
import os

def connect_to_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Northwind_small.sqlite')
    db_path = os.path.abspath(db_path)
    conn = sqlite3.connect(db_path)
    print("✅ Connected to SQLite DB")
    return conn
