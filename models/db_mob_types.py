from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base

class DBMOBType(Base):
    __tablename__ = "mob_types"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]]
    mobs = None

    def __repr__(self) -> str:
        return f"DBMOBType(id={self.id!r}, type={self.type!r})"