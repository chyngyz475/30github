from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP, BigInteger
from database import Base
import datetime

class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    battery = Column(Integer, nullable=True)
    condition = Column(String, nullable=False)
    status = Column(String, default="Активно")
    description = Column(Text, nullable=True)
    photos = Column(JSON, nullable=False)  # Сохраняем ссылки на фото
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"Phone(brand={self.brand}, model={self.model}, price={self.price})"


class Subscriber(Base):
    __tablename__ = "subscribers"

    user_id = Column(BigInteger, primary_key=True, index=True)  # Уникальный ID пользователя в Telegram
    first_name = Column(String, nullable=False)  # Имя пользователя
    last_name = Column(String, nullable=True)  # Фамилия пользователя (необязательно)
    username = Column(String, nullable=True)  # Юзернейм Telegram
    phone_number = Column(String, nullable=True)  # Номер телефона
    subscribed_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)  # Время подписки
    is_active = Column(Integer, default=1)  # Статус подписки (активен/неактивен)

    def __repr__(self):
        return f"Subscriber(user_id={self.user_id}, first_name={self.first_name}, is_active={self.is_active})"
