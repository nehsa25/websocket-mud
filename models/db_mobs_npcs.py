from sqlalchemy import ForeignKey, String
from models.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class DBNpc(Base):
    __tablename__ = "npc_mobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mob_id: Mapped[int] = mapped_column(ForeignKey("mobs.id"), unique=True, nullable=False)
    title: Mapped[Optional[str]]
    interests: Mapped[Optional[str]]
    npc_type: Mapped[str] = mapped_column(String, nullable=False)
    wanders: Mapped[Optional[bool]]    
    mob = None

    def __repr__(self) -> str:
        return f"DBNpc(id={self.id!r}, title={self.title!r})"