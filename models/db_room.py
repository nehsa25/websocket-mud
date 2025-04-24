from models.base import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class DBRoom(Base):
    __tablename__ = "rooms"
    name = Column(String, primary_key=True)
    description = Column(String)
    inside = Column(Boolean)
    npcs = relationship("DBNpc", back_populates="room")
    monsters = relationship("DBMonster", back_populates="room")
    items = relationship("DBItem", back_populates="room")
    players = relationship("DBPlayer", back_populates="room")
    exits = relationship("DBExit", foreign_keys="[DBExit.from_room_name]", back_populates="from_room")

    def __repr__(self):
        return f"<DBRoom(name='{self.name}')>"
