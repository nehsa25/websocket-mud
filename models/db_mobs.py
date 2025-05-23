from sqlalchemy import String, ForeignKey
from models.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBMob(Base):
    """For NehsaMUD, a MOB is the base that all other types are based on player, npc, monster.
    The purpose of this is to allow in the future for a player to be able to play as a monster or npc.
    This is not implemented yet."""

    __tablename__ = "mobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True, unique=True)
    pronoun: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    experience: Mapped[Optional[int]]
    experience: Mapped[int]
    level: Mapped[int]
    money: Mapped[int]
    title: Mapped[Optional[str]]
    alignment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("alignments.id"))
    attributes_id: Mapped[Optional[int]] = mapped_column(ForeignKey("attributes.id"))
    race_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_races.id"))
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    mob_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("mob_types.id"))
    room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rooms.id"))
    player_race_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    player_class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    attributes = None
    npc = None
    player = None
    monster = None
    player_race = None
    player_class = None
    mob_type = None
    directives = None
    room = None
    alignment = None
    room = None
    player = None

    def __repr__(self) -> str:
        return f"DBMob(id={self.id!r}, name={self.name!r})"
