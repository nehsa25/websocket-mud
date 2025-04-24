from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from models.base import Base


class DBWeapon(Base):
    __tablename__ = "weapon"

    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    damage = Column(Integer)
    weapon_type = Column(String)
    speed = Column(Integer)

    item = relationship("DBItem", back_populates="weapon")
