# models/db_directives.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import Base
from models.association_tables import DBAssociations

class DBDirectives(Base):
    __tablename__ = "directives"

    id = Column(Integer, primary_key=True, autoincrement=True)
    summary = Column(Text)
    directive_type = Column(String)
    value = Column(String)
    mobs = None

    def __repr__(self):
        return f"<DBDirectives(id={self.id}, type='{self.directive_type}')>"