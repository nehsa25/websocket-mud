from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import Base

class DBFood(Base):
    __tablename__ = "food"
    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    freshness = Column(Integer)

    item = relationship("DBItem", back_populates="food")

    def __repr__(self):
        return f"<DBFood(item_id={self.item_id})>"