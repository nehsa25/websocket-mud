from sqlalchemy import Boolean, String, Table, Column, Integer, ForeignKey
from models.base import Base

class DBAssociations:
    mob_directives_association = Table(
        "mob_directives",
        Base.metadata,
        Column("mob_id", Integer, ForeignKey("mobs.id"), primary_key=True),
        Column("directive_id", Integer, ForeignKey("directives.id"), primary_key=True),
    )

    npc_directives_association = Table(
        "npc_directives",
        Base.metadata,
        Column("npc_id", Integer, ForeignKey("npcs.id"), primary_key=True),
        Column("directive_id", Integer, ForeignKey("directives.id"), primary_key=True),
    )

    monster_directives_association = Table(
        "monster_directives",
        Base.metadata,
        Column("monster_id", Integer, ForeignKey("monsters.id"), primary_key=True),
        Column("directive_id", Integer, ForeignKey("directives.id"), primary_key=True),
    )

    race_directives_association = Table(
        "race_directives",
        Base.metadata,
        Column("race_id", Integer, ForeignKey("player_race.id"), primary_key=True),
        Column("directive_id", Integer, ForeignKey("directives.id"), primary_key=True),
    )

    class_directives_association = Table(
        "class_directives",
        Base.metadata,
        Column("class_id", Integer, ForeignKey("player_class.id"), primary_key=True),
        Column("directive_id", Integer, ForeignKey("directives.id"), primary_key=True),
    )

    room_items_association = Table(
        "room_items",
        Base.metadata,
        Column("room_name", String, ForeignKey("rooms.name"), primary_key=True),
        Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
        Column("is_hidden", Boolean, default=False),
    )

    item_effects_association = Table(
        "item_effects",
        Base.metadata,
        Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
        Column("effect_id", Integer, ForeignKey("effects.id"), primary_key=True),
    )