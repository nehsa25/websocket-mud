from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import Base


class DBDirectives(Base):
    __tablename__ = "directives"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mob_id = Column(Integer, ForeignKey("npcs.id"), nullable=True)
    monster_id = Column(Integer, ForeignKey("monsters.id"), nullable=True)
    summary = Column(Text)
    directive_type = Column(String)
    value = Column(String)

    npc = relationship("DBNpc", back_populates="directives")
    monster = relationship("DBMonster", back_populates="directives")

    def __repr__(self):
        return f"<DBDirective(npc_id={self.npc_id}, type='{self.directive_type}', key='{self.key}')>"
