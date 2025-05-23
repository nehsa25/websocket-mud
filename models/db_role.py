from sqlalchemy import String
from models.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBRole(Base):

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"DBRole(id={self.id!r}, name={self.name!r})"