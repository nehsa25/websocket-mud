# models/db_monster.py
from typing import Optional
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBMonster(Base):
    __tablename__ = "monsters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mob_id: Mapped[int] = mapped_column(ForeignKey("mobs.id"), unique=True, nullable=False)
    possible_adjectives: Mapped[Optional[str]]
    adjective_chance: Mapped[Optional[int]]


    mob = None
    directives = None

    def __repr__(self) -> str:
        return f"DBMonster(id={self.id!r}, type={self.type!r})"
