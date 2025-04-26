from enum import Enum


class AlignmentEnum(Enum):
    GOOD = "good"  # attacks evil players only
    NEUTRAL = "neutral" # only attacks if attacked
    EVIL = "evil"  # attacks good players only
    CHAOTIC = "chaotic" # attacks all players
