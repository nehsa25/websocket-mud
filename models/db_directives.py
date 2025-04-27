from typing import Optional

from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBDirectives(Base):
    __tablename__ = "directives"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    mobs = None

    def __repr__(self) -> str:
        return f"DBDirectives(id={self.id!r}, type={self.directive_type!r})"
