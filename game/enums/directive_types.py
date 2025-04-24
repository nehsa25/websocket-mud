from enum import Enum


class DirectiveTypes(Enum):
    """Enum for directives that can be used in the game. NPCs will use AI and these will inform the engine
    how to respond to the player. These are keywords at the beginning of the full directive string."""

    BEHAVIOR = "behavior"
