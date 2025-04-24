# number of monsters in the room
from enum import Enum


class RoomDanger(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 1
    MEDHIGH = 3
    HIGH = 4
    EXTREME = 5
    RANDOM = 6
