from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData
from models.base import Base

metadata_obj = MetaData()

room_items = Table(
    "room_items",
    metadata_obj,
    Column("room_name", String, ForeignKey("rooms.name"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("is_hidden", Boolean, default=False),
)

item_effects = Table(
    "item_effects",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("effect_id", Integer, ForeignKey("effects.id"), primary_key=True),
)


class DBItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    item_type = Column(String)
    weight = Column(Float, nullable=False)
    verb = Column(String)
    plural_verb = Column(String)
    description = Column(String)
    room_name = Column(String, ForeignKey("rooms.name"))
    room = relationship("DBRoom", back_populates="items")
    armor = relationship("DBArmor", uselist=False, back_populates="item",  foreign_keys="[DBArmor.id]")
    food = relationship("DBFood", uselist=False, back_populates="item",  foreign_keys="[DBFood.id]")
    lightsource = relationship("DBLightsource", uselist=False, back_populates="item",  foreign_keys="[DBLightsource.id]")
    weapon = relationship("DBWeapon", uselist=False, back_populates="item",  foreign_keys="[DBWeapon.id]")
    effects = relationship("DBEffect", secondary=item_effects, back_populates="items")

    def __repr__(self):
        return f"<DBItem(name='{self.name}', type='{self.item_type}')>"