from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import config

DATABASE_URL = f"postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Функция для создания сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
