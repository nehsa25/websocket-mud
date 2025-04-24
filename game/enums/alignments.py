from enum import Enum


class Alignment(Enum):
    GOOD = 1  # attacks evil players only
    NEUTRAL = 2  # only attacks if attacked
    EVIL = 3  # attacks good players only
    CHOATIC = 4  # attacks all players
