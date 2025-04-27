# models/db_room.py
from typing import Optional
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBRoom(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    inside: Mapped[Optional[bool]]
    npcs = None
    monsters = None
    items = None
    players = None
    exits = None

    def __repr__(self) -> str:
        return f"DBRoom(name={self.name!r})"