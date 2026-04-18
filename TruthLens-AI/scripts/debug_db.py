import sqlite3
import os
import sys
from pathlib import Path

# Add project root to sys.path so we can import backend.auth
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.auth import init_db, DATABASE

def verify():
    print(f"Triggering init_db() for migration...")
    init_db()
    
    print(f"Checking database at: {DATABASE}")
    conn = sqlite3.connect(str(DATABASE))
    cursor = conn.execute("PRAGMA table_info(users)")
    cols = [row[1] for row in cursor.fetchall()]
    print(f"Current columns in 'users' table: {cols}")
    
    if 'created_at' in cols:
        print("SUCCESS: 'created_at' column exists.")
    else:
        print("FAILURE: 'created_at' column is still missing.")
    
    cursor = conn.execute("SELECT id, username, role, created_at FROM users LIMIT 5")
    rows = cursor.fetchall()
    print("Sample user data (id, username, role, created_at):")
    for row in rows:
        print(row)

if __name__ == "__main__":
    verify()
