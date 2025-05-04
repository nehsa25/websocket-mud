from enum import Enum, auto


class SendScopeEnum(Enum):
    PLAYER = auto()
    ROOM = auto() # the room the player is in
    ENVIRONMENT = auto() # the town of Smee
    WORLD = auto() # everyone in the world
