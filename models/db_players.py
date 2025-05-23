
from typing import List
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey

from models.db_characters import DBCharacter


class DBPlayer(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    pin: Mapped[str]
    salt: Mapped[str]
    email: Mapped[str]
    characters = Mapped[List["DBCharacter"]]

    def __repr__(self) -> str:
        return f"DBPlayer(id={self.id!r})"
