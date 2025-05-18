# models/db_room.py
from typing import Optional
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBRoom(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]
    environment_id: Mapped[Optional[int]]
    description: Mapped[Optional[str]]
    inside: Mapped[Optional[bool]]
    exits_id: Mapped[Optional[int]]
    npcs = None
    monsters = None
    items = None
    characters = None
    exits = None

    def __repr__(self) -> str:
        return f"DBRoom(name={self.name!r})"