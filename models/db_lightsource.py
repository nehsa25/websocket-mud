from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class DBLightsource(Base):
    __tablename__ = "lightsource"

    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    quality = Column(Integer)
    brightness = Column(Integer)

    item = relationship("DBItem", back_populates="lightsource")
