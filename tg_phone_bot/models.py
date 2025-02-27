from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP
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