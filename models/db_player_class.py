from sqlalchemy import Column, String, Integer

from models.base import Base


class DBPlayerClass(Base):
    __tablename__ = "player_class"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    abilities = Column(String)
    base_experience_adjustment = Column(Integer)

    def __repr__(self):
        return f"<DBPlayerClass(name='{self.name}')>"
