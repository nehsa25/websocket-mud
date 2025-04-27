from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base

class DBEffect(Base):
    __tablename__ = "effects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String)
    items = None

    def __repr__(self) -> str:
        return f"DBEffect(id={self.id!r}, keyword={self.keyword!r})"
