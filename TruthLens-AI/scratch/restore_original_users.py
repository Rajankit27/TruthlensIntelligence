import pymongo
import os
import datetime
from werkzeug.security import generate_password_hash

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "truthlens"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]

print("Restoring original user accounts...")

# Clear any existing users to avoid DuplicateKeyError
users_col.delete_many({})

users_to_restore = [
    {
        "username": "admin",
        "password": "admin",
        "role": "admin"
    },
    {
        "username": "Ankit",
        "password": "admin",
        "role": "user"
    },
    {
        "username": "RajAnkit27",
        "password": "RajAnkit27@",
        "role": "user"
    }
]

for u in users_to_restore:
    doc = {
        "username": u["username"],
        "password_hash": generate_password_hash(u["password"]),
        "role": u["role"],
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    users_col.insert_one(doc)
    print(f"Restored user: {u['username']}")

print("Restoration complete. All users can now login with their original credentials.")
