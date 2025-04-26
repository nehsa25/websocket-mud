from enum import Enum


class CommandEnum(Enum):
    LOOK = "look"
    MOVE = "move"
    ATTACK = "attack"
    GET = "get"
    INVENTORY = "inventory"
    DROP = "drop"
    SEARCH = "search"
    HIDE = "hide"
    STASH = HIDE
    EQUIP = "equip"
    STATISTICS = "statistics"
    EXPERIENCE = "experience"
    LOOT = "loot"
    WHO = "who"
    REST = "rest"
    SAY = "say"
    SYSTEM = "system"
    HELP = "help"
    QUIT = "quit"
    YELL = "yell"
    TELEPATHY = "telepathy"
    WHISPER = "whisper"
    EMOTE = "emote" # emote sadness: <person> slumps shoulders in sadness
