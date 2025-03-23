import psycopg2
import config

try:
    conn = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
        host=config.DB_HOST
    )
    print("✅ Успешное подключение к базе данных!")
    conn.close()
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")