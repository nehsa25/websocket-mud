# models/db_effect.py
from sqlalchemy import Column, Integer, String
from models.base import Base

class DBEffect(Base):
    __tablename__ = "effects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String, nullable=False, unique=True)
    description = Column(String)
    items = None

    def __repr__(self):
        return f"<DBEffect(keyword='{self.keyword}')>"