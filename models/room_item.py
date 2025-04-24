from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base import Base
from models.db_item import DBItem
from models.db_room import DBRoom
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class RoomItem(Base):
    __tablename__ = "room_items"
    room_name = Column(String, ForeignKey("rooms.name"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    is_hidden = Column(Boolean, default=False)

    item = relationship("DBItem")
    room = relationship("DBRoom", back_populates="items") # Add relationship here

    async def process_room_contents(session: AsyncSession, room: DBRoom):
        """
        An example function that might use the RoomItem class
        to retrieve and process items in a given room.
        """
        items_in_room = (
            await session.execute(select(DBItem).join(RoomItem).where(RoomItem.room_name == room.name)).scalars().all()
        )

        print(f"Items in {room.name}:")
        for item in items_in_room:
            print(f"- {item.name} ({item.description})")


    async def add_item_to_room(session: AsyncSession, room: DBRoom, item: DBItem, is_hidden: bool = False):
        """
        An example function that might use the RoomItem class
        to add an item to a room.
        """
        room_item = RoomItem(room=room, item=item, is_hidden=is_hidden)
        session.add(room_item)
        await session.commit()
