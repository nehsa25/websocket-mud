import asyncio
from enum import Enum
import inspect
import random
import time
from aiimages import AIImages
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility


class MudDirections:  # directions
    up = ("u", "Up")
    down = ("d", "Down")
    north = ("n", "North")
    south = ("s", "South")
    east = ("e", "East")
    west = ("w", "West")
    northwest = ("nw", "Northwest")
    northeast = ("ne", "Northeast")
    southeast = ("se", "Southeast")
    southwest = ("sw", "Southwest")
    directions = [
        up[0].lower(),
        up[1].lower(),
        down[0].lower(),
        down[1].lower(),
        north[0].lower(),
        north[1].lower(),
        south[0].lower(),
        south[1].lower(),
        east[0].lower(),
        east[1].lower(),
        west[0].lower(),
        west[1].lower(),
        northwest[0].lower(),
        northwest[1].lower(),
        northeast[0].lower(),
        northeast[1].lower(),
        southeast[0].lower(),
        southeast[1].lower(),
        southwest[0].lower(),
        southwest[1].lower(),
    ]
    pretty_directions = [
        up,
        down,
        north,
        south,
        east,
        west,
        northwest,
        northeast,
        southeast,
        southwest,
    ]

    opp_directions = [
        (up, down),
        (east, west),
        (north, south),
        (northeast, southwest),
        (northwest, southeast),
    ]


class Room(Utility):
    # number of monsters in the room
    class Scariness(Enum):
        NONE = 0
        LOW = 1
        MEDIUM = 1
        MEDHIGH = 3
        HIGH = 4
        EXTREME = 5
        POOP = 6
        
    dirs = MudDirections()
    id: 0
    name = ""
    inside = False
    description = ""
    monster_spawn = False
    monster_saturation = 0.7
    scariness = 0
    environment = (None,)
    exits = ([],)
    items = ([],)
    hidden_items = ([],)
    monsters = ([],)
    players = ([],)
    npcs = []

    def __init__(
        self,
        id,
        name,
        inside,
        description,
        exits,
        environment,
        scariness,
        logger,
        items=[],
        hidden_items=[],
        monsters=[],
        players=[],
        npcs=[],
    ) -> None:
        self.id = id
        self.name = name
        self.inside = inside
        self.description = description
        self.exits = exits
        self.environment = environment
        self.items = items
        self.hidden_items = hidden_items
        self.monsters = monsters
        self.players = players
        self.npcs = npcs
        self.logger = logger
        self.scariness = random.choice(list(self.Scariness)).value
        LogUtils.debug(f"Initializing RoomFactory() class", self.logger)

    async def alert(
        self, message, exclude_player=False, player=None, event_type=MudEvents.InfoEvent
    ):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, message: {message}", self.logger)
        for p in self.players:
            if exclude_player and player is not None:
                if p.name != player.name:
                    LogUtils.info(
                        f'{method_name}: alerting {p.name} of "{message}"', self.logger
                    )
                    await self.send_message(event_type(message), p.websocket)
            else:
                await self.send_message(event_type(message), p.websocket)


class RoomFactory(Utility):
    environment = None

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug(f"Initializing Room() class", self.logger)

    def add_room(
        self,
        id,
        name,
        inside,
        description,
        exits,
        environment,
        items=[],
        hidden_items=[],
        monsters=[],
        players=[],
        npcs=[],
    ):
        method_name = inspect.currentframe().f_code.co_name
        
        scariness = random.choice(list(Room.Scariness)).value
        room = Room(
            id,
            name,
            inside,
            description,
            exits,
            environment,
            scariness,
            items=items,
            hidden_items=hidden_items,
            monsters=monsters,
            players=players,
            npcs=npcs,
            logger=self.logger,
        )
        LogUtils.debug(f"{method_name}: generated room: {room}", self.logger)
        return room
