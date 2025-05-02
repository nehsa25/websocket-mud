# models/db_player_class.py
from typing import Optional
from sqlalchemy import String
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBPlayerClass(Base):
    __tablename__ = "player_classes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String)
    abilities: Mapped[Optional[str]] = mapped_column(String)
    directives: Mapped[Optional[str]] = mapped_column(String)
    base_experience_adjustment: Mapped[Optional[int]]
    playable: Mapped[Optional[bool]] = mapped_column(default=True)

    mobs = None

    def __repr__(self) -> str:
        return f"DBPlayerClass(id={self.id!r}, name={self.name!r})"