from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class DBArmorTypes(Base):
    __tablename__ = "armor_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    item = relationship("DBArmor", back_populates="armor_type")

    def __repr__(self):
        return f"<DBArmor(item_id={self.id}, type='{self.armor_type}')>"
