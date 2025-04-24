from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base


class DBExit(Base):
    __tablename__ = "exits"
    from_room_name = Column(String, ForeignKey("rooms.name"), primary_key=True)
    to_room_name = Column(String, ForeignKey("rooms.name"), primary_key=True)
    direction = Column(String, primary_key=True)

    from_room = relationship("DBRoom", foreign_keys=[from_room_name], back_populates="exits")
    to_room = relationship("DBRoom", foreign_keys=[to_room_name], backref="incoming_exits")
