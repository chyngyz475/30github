 
# models.py

import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
    
    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                card_numbers TEXT,
                phone_numbers TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_data(self, data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO scraped_data (url, card_numbers, phone_numbers)
            VALUES (?, ?, ?)
        """, (data['url'], ', '.join(data['card_numbers']), ', '.join(data['phone_numbers'])))
        conn.commit()
        conn.close()

    def is_duplicate(self, url):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM scraped_data WHERE url = ?", (url,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
