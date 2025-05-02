# models/db_environment.py
from typing import Optional
from sqlalchemy import String
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class DBEnvironment(Base):
    __tablename__ = "environments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String)
    spawn_monsters: Mapped[Optional[bool]]
    spawn_guards: Mapped[Optional[bool]]

    def __repr__(self) -> str:
        return f"DBEnvironment(id={self.id!r}, name={self.name!r})"