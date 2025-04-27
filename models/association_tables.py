from sqlalchemy import Boolean, String, Table, Column, Integer, ForeignKey
from models.base import Base

class DBAssociations:
    mob_directives_association = Table(
        "mob_directives",
        Base.metadata,
        Column("mob_id", Integer, ForeignKey("mobs.id"), primary_key=True),
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