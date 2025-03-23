from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP, BigInteger, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    condition = Column(String, nullable=False)
    battery = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    photos = Column(JSON, nullable=False)  # Список file_id или путей
    status = Column(String, default="active")  # active, reserved, sold
    created_at = Column(TIMESTAMP, default=func.now())

    def __repr__(self):
        return f"Phone(brand={self.brand}, model={self.model}, price={self.price})"

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    phone_id = Column(Integer, ForeignKey("phones.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="new")  # new, processing, completed
    created_at = Column(TIMESTAMP, default=func.now())

    def __repr__(self):
        return f"Request(phone_id={self.phone_id}, user_id={self.user_id}, status={self.status})"

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)  # Telegram user_id
    first_name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    role = Column(String, default="user")  # user, admin
    registered_at = Column(TIMESTAMP, default=func.now())

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, role={self.role})"