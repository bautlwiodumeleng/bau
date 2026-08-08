import sqlite3

conn = sqlite3.connect("instance/database.db")
cursor = conn.cursor()

print("=== USERS TABLE ===")
cursor.execute("PRAGMA table_info(users)")
for row in cursor.fetchall():
    print(row)

conn.close()