import sys
import os

# Make sure parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.db_connect import connect_to_db
import pandas as pd

conn = connect_to_db()

query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query, conn)

print("📦 Tables in the DB:")
print(tables)
