import json
from config import JSON_DB_PATH

def save_account(email, password):
    try:
        with open(JSON_DB_PATH, "r", encoding="utf-8") as file:
            db = json.load(file)
    except FileNotFoundError:
        db = {"accounts": []}

    db["accounts"].append({"email": email, "password": password})
    
    with open(JSON_DB_PATH, "w", encoding="utf-8") as file:
        json.dump(db, file, indent=4, ensure_ascii=False)

def get_account():
    try:
        with open(JSON_DB_PATH, "r", encoding="utf-8") as file:
            db = json.load(file)
            return db["accounts"][0] if db["accounts"] else None
    except FileNotFoundError:
        return None
