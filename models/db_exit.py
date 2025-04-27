# models/db_exit.py
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBExit(Base):
    __tablename__ = "exits"

    from_room_name: Mapped[str] = mapped_column(ForeignKey("rooms.name"), primary_key=True)
    to_room_name: Mapped[str] = mapped_column(ForeignKey("rooms.name"), primary_key=True)
    direction: Mapped[str] = mapped_column(primary_key=True)
    from_room = None
    to_room = None

    def __repr__(self) -> str:
        return f"DBExit(direction={self.direction!r})"