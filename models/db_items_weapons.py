from typing import Optional
from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBWeapon(Base):
    __tablename__ = "weapon_items"
    id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    damage: Mapped[Optional[str]]
    quality: Mapped[Optional[int]]
    speed: Mapped[Optional[int]]
    item = None

    def __repr__(self) -> str:
        return f"DBWeapon(id={self.id}, damage={self.damage}, quality={self.quality}, speed={self.speed})"