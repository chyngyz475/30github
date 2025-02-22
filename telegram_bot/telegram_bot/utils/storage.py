import json
from config import JSON_DB_PATH

def save_data(data):
    try:
        with open(JSON_DB_PATH, "r", encoding="utf-8") as file:
            db = json.load(file)
    except FileNotFoundError:
        db = []

    db.append(data)
    with open(JSON_DB_PATH, "w", encoding="utf-8") as file:
        json.dump(db, file, indent=4, ensure_ascii=False)
