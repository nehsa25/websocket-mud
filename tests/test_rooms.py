import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, ForeignKey
from typing import List, Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, sessionmaker

from models.db_items import DBItem

# --- Define your SQLAlchemy models here ---
# models/base.py
Base = declarative_base()

# models/db_room.py
class DBRoom(Base):
    __tablename__ = "rooms"
    name: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[Optional[str]]
    inside: Mapped[Optional[bool]]
    npcs: Mapped[List["DBNpc"]] = relationship(back_populates="room", primaryjoin="DBRoom.name == DBNpc.room_name")
    monsters: Mapped[List["DBMonster"]] = relationship(back_populates="room", primaryjoin="DBRoom.name == DBMonster.room_name")
    items: Mapped[List["DBItem"]] = relationship(back_populates="room")
    players: Mapped[List["DBPlayer"]] = relationship(back_populates="room")
    exits: Mapped[List["DBExit"]] = relationship(foreign_keys="[DBExit.from_room_name]", back_populates="from_room")

    def __repr__(self) -> str:
        return f"DBRoom(name={self.name!r})"

# models/db_exit.py
class DBExit(Base):
    __tablename__ = "exits"
    from_room_name: Mapped[str] = mapped_column(ForeignKey("rooms.name"), primary_key=True)
    to_room_name: Mapped[str] = mapped_column(ForeignKey("rooms.name"), primary_key=True)
    direction: Mapped[str] = mapped_column(primary_key=True)

    from_room: Mapped["DBRoom"] = relationship(foreign_keys=[from_room_name], back_populates="exits")
    to_room: Mapped["DBRoom"] = relationship(foreign_keys=[to_room_name], backref="incoming_exits")

    def __repr__(self) -> str:
        return f"DBExit(direction={self.direction!r})"

# models/db_npc.py
class DBNpc(Base):
    __tablename__ = "npcs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mob_id: Mapped[int] = mapped_column(ForeignKey("mobs.id"), unique=True, nullable=False)
    room_name: Mapped[Optional[str]] = mapped_column(ForeignKey("rooms.name"))
    mob: Mapped["DBMob"] = relationship(back_populates="npc")
    room: Mapped["DBRoom"] = relationship(back_populates="npcs")
    def __repr__(self) -> str:
        return f"DBNpc(id={self.id!r})"

# models/db_monster.py
class DBMonster(Base):
    __tablename__ = "monsters"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mob_id: Mapped[int] = mapped_column(ForeignKey("mob.id"), unique=True, nullable=False)
    room_name: Mapped[Optional[str]] = mapped_column(ForeignKey("rooms.name"))
    mob: Mapped["DBMob"] = relationship(back_populates="monster")
    def __repr__(self) -> str:
        return f"DBMonster(id={self.id!r})"

# models/db_player.py
class DBPlayer(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    mob_id: Mapped[int] = mapped_column(ForeignKey("mob.id"), unique=True, nullable=False)
    room_name: Mapped[Optional[str]] = mapped_column(ForeignKey("rooms.name"))
    mob: Mapped["DBMob"] = relationship(back_populates="player")
    def __repr__(self) -> str:
        return f"DBPlayer(id={self.id!r})"

# models/db_mob.py
class DBMob(Base):
    __tablename__ = "mobs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    room_name: Mapped[Optional[str]] = mapped_column(ForeignKey("rooms.name"))

    npc: Mapped[Optional["DBNpc"]] = relationship(back_populates="mob")
    player: Mapped[Optional["DBPlayer"]] = relationship(back_populates="mob")
    monster: Mapped[Optional["DBMonster"]] = relationship(back_populates="mob")

    def __repr__(self) -> str:
        return f"DBMob(id={self.id!r}, name={self.name!r})"


# --- Test Setup ---
@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")  # Use an in-memory SQLite database for testing
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    test_session = Session()

    # Populate with some test data
    room1 = DBRoom(name="Room 1", description="Description of Room 1")
    room2 = DBRoom(name="Room 2", description="Description of Room 2")
    room3 = DBRoom(name="Room 3", description="Description of Room 3")
    test_session.add_all([room1, room2, room3])
    test_session.commit()

    exit1_2 = DBExit(from_room_name="Room 1", to_room_name="Room 2", direction="east")
    exit2_1 = DBExit(from_room_name="Room 2", to_room_name="Room 1", direction="west")
    exit1_3 = DBExit(from_room_name="Room 1", to_room_name="Room 3", direction="north")
    exit3_1 = DBExit(from_room_name="Room 3", to_room_name="Room 1", direction="south")
    test_session.add_all([exit1_2, exit2_1, exit1_3, exit3_1])
    test_session.commit()
    yield test_session
    test_session.close()
    Base.metadata.drop_all(engine)


# --- Tests ---
def test_room_exits_are_valid(session):
    rooms = session.execute(select(DBRoom)).scalars().all()
    assert len(rooms) > 0, "No rooms found in the database"
    for room in rooms:
        print(f"Checking exits for room: {room.name}")
        for exit_ in room.exits:
            print(f"  - Exit: {exit_.direction} to {exit_.to_room_name}")
            to_room = session.get(DBRoom, exit_.to_room_name)
            assert to_room is not None, f"Exit in room '{room.name}' points to non-existent room '{exit_.to_room_name}'"

def test_bidirectional_exits(session):
    rooms = session.execute(select(DBRoom)).scalars().all()
    for room in rooms:
        for exit_ in room.exits:
            reverse_direction = get_reverse_direction(exit_.direction)
            reverse_exit = session.execute(
                select(DBExit).where(DBExit.from_room_name == exit_.to_room_name,
                                     DBExit.to_room_name == exit_.from_room_name,
                                     DBExit.direction == reverse_direction)
            ).scalar_one_or_none()
            assert reverse_exit is not None, (
                f"Room '{room.name}' has an exit '{exit_.direction}' to '{exit_.to_room_name}', "
                f"but '{exit_.to_room_name}' does not have a corresponding '{reverse_direction}' exit back to '{room.name}'"
            )

def get_reverse_direction(direction: str) -> str:
    """Helper function to get the reverse direction."""
    if direction == "north": 
        return "south"
    elif direction == "south": 
        return "north"
    elif direction == "east": 
        return "west"
    elif direction == "west": 
        return "east"
    elif direction == "northeast": 
        return "southwest"
    elif direction == "northwest": 
        return "southeast"
    elif direction == "southeast": 
        return "northwest"
    elif direction == "southwest": 
        return "northeast"
    elif direction == "up": 
        return "down"
    elif direction == "down": 
        return "up"
    return ""
