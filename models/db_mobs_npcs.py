from sqlalchemy import ForeignKey
from models.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class DBNpc(Base):
    __tablename__ = "npcs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mob_id: Mapped[int] = mapped_column(ForeignKey("mobs.id"), unique=True, nullable=False)
    interests: Mapped[Optional[str]]
    wanders: Mapped[Optional[bool]]
    death_cry: Mapped[Optional[str]]
    entrance_cry: Mapped[Optional[str]]
    victory_cry: Mapped[Optional[str]]
    flee_cry: Mapped[Optional[str]]
    respawn_rate_secs: Mapped[Optional[int]]

    attributes = None    
    mob = None
    directives = None

    def __repr__(self) -> str:
        return f"DBNpc(id={self.id!r}, title={self.title!r})"