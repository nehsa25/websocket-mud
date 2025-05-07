from typing import Optional

from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBPlayer(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    experience: Mapped[int]
    level: Mapped[int]
    token: Mapped[str]
    money: Mapped[int]
    pin: Mapped[str]
    salt: Mapped[str]
    pronoun: Mapped[str]
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("roles.id"))
    race_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    attributes_id: Mapped[Optional[int]] = mapped_column(ForeignKey("attributes.id"))
    alignment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("alignments.id"))
    room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rooms.id"))
    attributes = None
    race = None
    player_class = None
    room = None
    

    def __repr__(self) -> str:
        return f"DBPlayer(id={self.id!r})"
