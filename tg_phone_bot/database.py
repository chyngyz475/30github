from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

# URL для подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql://chyngyz:xsyusp0411@127.0.0.1:5432/phone_korea"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)
