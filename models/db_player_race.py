from sqlalchemy import Column, Integer, String

from models.base import Base


class DBPlayerRace(Base):
    __tablename__ = "player_race"

    id = Column(Integer, primary_key=True, autoincrement=True)
    race_name = Column(String)
    description = Column(String)
    abilities = Column(String)

    def __repr__(self):
        return f"<DBPlayerRace(race_name='{self.race_name}')>"
