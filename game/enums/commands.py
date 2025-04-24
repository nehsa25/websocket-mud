from enum import Enum


class Commands(Enum):
    LOOK = 1
    MOVE = 2
    ATTACK = 3
    GET = 4
    INVENTORY = 5
    DROP = 6
    SEARCH = 7
    HIDE = 8
    STASH = HIDE
    EQUIP = 10
    STATISTICS = 11
    EXPERIENCE = 12
    LOOT = 13
    WHO = 14
    REST = 15
    SAY = 16
    SYSTEM = 17
    HELP = 18
    QUIT = 19
    YELL = 20
    TELEPATHY = 21
    WHISPER = 22
