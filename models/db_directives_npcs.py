from typing import Optional
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.base import Base

class DBDirectivesNpcs(Base):
    """Model for directives that are associated with NPCs"""
    __tablename__ = "directives_npcs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    directive: Mapped[Optional[Text]] = mapped_column(Text)
    directive_type: Mapped[Optional[str]] = mapped_column(String)

    directives =  None

    def __repr__(self) -> str:
        return f"DBDirectivesNpcs(id={self.id!r}, type={self.directive_type!r})"
