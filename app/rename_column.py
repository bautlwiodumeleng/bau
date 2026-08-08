import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE users
RENAME COLUMN company_name TO organisation_name;
""")

conn.commit()
conn.close()

print("Column renamed successfully.")