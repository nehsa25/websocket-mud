# models/db_player_race.py
from typing import Optional
from sqlalchemy import ForeignKey, String
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBPlayerRace(Base):
    __tablename__ = "player_races"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]]
    abilities: Mapped[Optional[str]]
    directives: Mapped[Optional[str]]
    base_experience_adjustment: Mapped[Optional[int]]
    attributes_id: Mapped[Optional[int]] = mapped_column(ForeignKey("attributes.id"))

    attributes: None
    mobs = None


    def __repr__(self) -> str:
        return f"DBPlayerRace(id={self.id!r}, race_name={self.race_name!r})"
