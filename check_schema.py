import sqlite3
import os

db_path = os.path.join("instance", "database.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

for table in ["users", "customers", "tasks"]:
    print(f"\n===== {table.upper()} =====")
    cursor.execute(f"PRAGMA table_info({table})")
    for row in cursor.fetchall():
        print(row)

conn.close()