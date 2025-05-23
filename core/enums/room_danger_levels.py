# number of monsters in the room
from enum import Enum


class RoomDangerEnum(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    MEDHIGH = "medhigh"
    HIGH = "high"
    EXTREME = "extreme"
    RANDOM = "random"
