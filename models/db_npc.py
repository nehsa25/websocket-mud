from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
import sqlalchemy as sa

from core.enums.npcs import NpcEnum
from models.base import Base


class DBNpc(Base):
    __tablename__ = "npcs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    title = Column(String)
    description = Column(String)
    interests = Column(sa.JSON)
    npc_type = Column(sa.Enum(NpcEnum), nullable=False)
    wanders = Column(Boolean)
    room_name = Column(String, ForeignKey("rooms.name"), nullable=False)
    room = relationship("DBRoom", back_populates="npcs")
    directives = relationship("DBDirectives", back_populates="npc")

    def __repr__(self):
        return f"<DBNpc(name='{self.name}')>"
