import sqlite3
import hashlib

def print_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('SELECT * FROM users')
    for row in cursor:
        print(f"ID: {row['id']}, Username: {row['username']}, Password: {row['password']}")
    conn.close()

print_users()
