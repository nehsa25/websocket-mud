# models/db_item.py
from typing import Optional
from sqlalchemy import String, Float, ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBItem(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    item_type: Mapped[Optional[str]]
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    verb: Mapped[Optional[str]]
    plural_verb: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    room_name: Mapped[Optional[str]] = mapped_column(ForeignKey("rooms.name"))
    room = None
    armor = None
    food = None
    lightsource = None
    weapon = None
    effects = None

    def __repr__(self) -> str:
        return f"DBItem(id={self.id!r}, name={self.name!r}, item_type={self.item_type!r})"
