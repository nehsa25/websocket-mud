from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base import Base

class DBArmor(Base):
    __tablename__ = "armor"

    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    armor_type = Column(String)

    item = relationship("DBItem", back_populates="armor")

    def __repr__(self):
        return f"<DBArmor(item_id={self.id}, type='{self.armor_type}')>"