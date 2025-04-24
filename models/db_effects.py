from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base

class DBEffect(Base):
    __tablename__ = "effects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String, nullable=False, unique=True)
    type = Column(Integer)

    items = relationship("DBItem", secondary="item_effects", back_populates="effects")

    def __repr__(self):
        return f"<DBEffect(keyword='{self.keyword}')>"