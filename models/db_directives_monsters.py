from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base

class DBDirectivesMonsters(Base):
    """Model for directives that are associated with monsters"""
    __tablename__ = "directives_monsters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    directive: Mapped[Optional[Text]] = mapped_column(Text)
    directive_type: Mapped[Optional[str]] = mapped_column(String)

    directives =  None

    def __repr__(self) -> str:
        return f"DBDirectivesMonsters(id={self.id!r}, type={self.directive_type!r})"
