from enum import Enum


class Directives(Enum):
    """Enum for directives that can be used in the game. NPCs will use AI and these will inform the engine
    how to respond to the player. These are keywords at the beginning of the full directive string."""

    LOW_THIEF = "I provide less change that I should 30 percent of the time."
    HIGH_THIEF = "I provide less change that I should 50 percent of the time."