# models/db_lightsource.py
from typing import Optional
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBLightsource(Base):
    __tablename__ = "lightsource_items"

    id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    brightness: Mapped[Optional[int]]
    item = None

    def __repr__(self) -> str:
        return f"DBLightsource(id={self.id!r}, quality={self.quality!r}, brightness={self.brightness!r})"
