import sqlite3
from pathlib import Path

DB_PATH = "database.db"  # Путь к базе данных

def get_db_connection():
    """Создает подключение к базе данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Для доступа к данным как к словарям
    return conn

def init_db():
    """Инициализация базы данных (создание таблиц)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Создаем таблицу пользователей, если она еще не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_user(username, email):
    """Функция для добавления нового пользователя."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    conn.commit()
    conn.close()
