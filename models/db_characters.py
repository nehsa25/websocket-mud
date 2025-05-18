from typing import Optional

from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBCharacter(Base):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    experience: Mapped[int]
    level: Mapped[int]
    money: Mapped[int]
    sex: Mapped[str]
    eye_brow: Mapped[str]
    eye_color: Mapped[str]
    body_type: Mapped[str]
    facial_hair: Mapped[Optional[str]]
    hair_color: Mapped[str]
    hair_style: Mapped[str]
    player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("players.id"))
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("roles.id"))
    player_race_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    player_class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    attributes_id: Mapped[Optional[int]] = mapped_column(ForeignKey("attributes.id"))
    alignment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("alignments.id"))
    room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rooms.id"))
    attributes = None
    player_race = None
    player_class = None
    room = None
    alignment = None
    role = None
    player = None
    

    def __repr__(self) -> str:
        return f"DBCharacter(id={self.id!r})"
