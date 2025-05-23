# models/db_armor.py
from typing import Optional
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBArmor(Base):
    __tablename__ = "armor"

    id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    armor_type: Mapped[Optional[str]]

    item = None

    def __repr__(self) -> str:
        return f"DBArmor(id={self.id!r}, armor_type={self.armor_type!r})"