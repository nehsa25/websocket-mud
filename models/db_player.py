from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class DBPlayer(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    room_name = Column(String, ForeignKey("rooms.name"))
    room = relationship("DBRoom", back_populates="players")
