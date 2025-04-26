from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class DBArmor(Base):
    __tablename__ = "armor"

    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    armor_type_id = Column(Integer, ForeignKey("armor_types.id"))  # This is correct

    item = relationship("DBItem", back_populates="armor")
    armor_type = relationship("DBArmorTypes", back_populates="item")

    def __repr__(self):
        return f"<DBArmor(item_id={self.id}, type='{self.armor_type}')>"
