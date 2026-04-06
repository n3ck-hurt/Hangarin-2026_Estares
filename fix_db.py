import sqlite3
import os

db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    tables = [
        'socialaccount_socialaccount', 
        'socialaccount_socialapp', 
        'socialaccount_socialtoken', 
        'socialaccount_socialapp_sites'
    ]
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE {table}")
            print(f"Dropped table: {table}")
        except sqlite3.OperationalError as e:
            print(f"Error dropping {table}: {e}")
    conn.commit()
    conn.close()
else:
    print("Database file not found.")
