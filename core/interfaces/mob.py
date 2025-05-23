from abc import ABC, abstractmethod
from typing import List

from core.data.room_data import RoomData


class MOBInterface(ABC):
    name: str
    title: str
    description: str
    common_phrases: List[str]
    interests: List[str]
    schedules: List[str]
    wander_event: object
    last_direction: str
    wanders: bool
    room: "RoomData"  # the quotes makes this a foward reference (it won't be evaluated until later thus preventing circular imports)
    prev_room_id: "RoomData"  # the quotes makes this a foward reference (it won't be evaluated until later thus preventing circular imports)
    last_check_combat: int
    alignment: bool
    in_combat: bool

    # announce we're here!
    @abstractmethod
    async def announce_entrance(self, room) -> None:
        pass

    @abstractmethod
    async def stop_combat(self):
        pass

    @abstractmethod
    async def break_combat(self, room):
        pass
    
    @abstractmethod
    async def killed(self, room):
        pass

    @abstractmethod
    async def respawn(self):
        pass

    @abstractmethod
    async def wander(self, is_npc):
        pass

    @abstractmethod
    async def check_combat(self):
        pass

    @abstractmethod
    async def speak(self, room):
        pass

    @abstractmethod
    async def move(self, direction, isNpc=True):
        pass
