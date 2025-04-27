# models/db_food.py
from typing import Optional
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBFood(Base):
    __tablename__ = "food_items"

    id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    freshness: Mapped[Optional[int]]
    item = None

    def __repr__(self) -> str:
        return f"DBFood(id={self.id!r}, freshness={self.freshness!r})"