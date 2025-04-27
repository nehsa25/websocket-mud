from typing import Optional
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBWeapon(Base):
    __tablename__ = "weapon_items"
    id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    damage: Mapped[Optional[int]]
    weapon_type: Mapped[Optional[str]]
    speed: Mapped[Optional[int]]
    item = None

    def __repr__(self) -> str:
        return f"DBWeapon(id={self.id!r}, damage={self.damage!r}, weapon_type={self.weapon_type!r}, speed={self.speed!r})"
