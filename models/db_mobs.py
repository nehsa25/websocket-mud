from sqlalchemy import String, ForeignKey
from models.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class DBMob(Base):

    __tablename__ = "mobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    pronoun: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    hitpoints: Mapped[Optional[int]]
    damage_potential: Mapped[Optional[str]]
    experience: Mapped[Optional[int]]
    money: Mapped[Optional[int]]
    player_race_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_races.id"))
    player_class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_classes.id"))
    mob_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey("mob_types.id"))
    npc_id: Mapped[Optional[int]] = mapped_column(ForeignKey("npc_mobs.mob_id"))
    monster_id: Mapped[Optional[int]] = mapped_column(ForeignKey("monster_mobs.mob_id"))
    player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("player_mobs.mob_id"))
    room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rooms.id"))
    npc  = None
    player = None
    monster = None
    player_race = None
    player_class = None
    mob_type = None
    directives = None
    room = None

    def __repr__(self) -> str:
        return f"DBMob(id={self.id!r}, name={self.name!r})"