from typing import Optional

from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBCharacter(Base):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    eye_brow: Mapped[str]
    eye_color: Mapped[str]
    body_type: Mapped[str]
    facial_hair: Mapped[Optional[str]]
    hair_color: Mapped[str]
    hair_style: Mapped[str]
    player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("players.id"))
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("roles.id"))
    mob_id: Mapped[Optional[int]] = mapped_column(ForeignKey("mobs.id"))

    role = None
    player = None
    
    def __repr__(self) -> str:
        return f"DBCharacter(id={self.id!r})"
