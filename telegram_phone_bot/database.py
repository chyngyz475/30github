import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}

async def init_db():
    conn = await asyncpg.connect(**DB_CONFIG)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            brand TEXT,
            model TEXT,
            price INTEGER,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    await conn.close()

async def get_db():
    return await asyncpg.connect(**DB_CONFIG)
