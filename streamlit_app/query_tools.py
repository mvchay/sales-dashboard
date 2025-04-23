
import sqlite3
import pandas as pd
import os

def get_db_connection():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'Northwind_small.sqlite'))
    return sqlite3.connect(db_path)

def run_query(query, conn=None):
    close_conn = False
    if conn is None:
        conn = get_db_connection()
        close_conn = True
    df = pd.read_sql_query(query, conn)
    if close_conn:
        conn.close()
    return df
