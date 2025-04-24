from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from models.base import Base


class DBMonster(Base):
    __tablename__ = "monsters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    pronoun = Column(String)
    type = Column(String)
    alignment = Column(String)
    description = Column(String)
    possible_adjectives = Column(String)
    adjective_chance = Column(Integer)
    respawn_rate_secs = Column(Integer)
    dead_epoch = Column(Integer)
    wanders = Column(Boolean)
    hitpoints = Column(Integer)
    damage_potential = Column(String)
    experience = Column(Integer)
    money = Column(Integer)
    death_cry = Column(String)
    entrance_cry = Column(String)
    victory_cry = Column(String)
    flee_cry = Column(String)
    room_name = Column(String, ForeignKey("rooms.name"), nullable=False)
    room = relationship("DBRoom", back_populates="monsters")
    directives = relationship("DBDirectives", back_populates="monster")
    

    def __repr__(self):
        return f"<DBMonster(name='{self.name}')>"
