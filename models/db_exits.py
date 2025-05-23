from sqlalchemy import String
from models.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBExit(Base):
    __tablename__ = "exits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    north: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    south: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    east: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    west: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    up: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    down: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    northeast: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    northwest: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    southeast: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    southwest: Mapped[Optional[int]] = mapped_column(String, nullable=True)
    room = None  # This will be set up in the relationships module

    def __repr__(self) -> str:
        return f"DBExit(id={self.id!r})"
