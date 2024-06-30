import asyncio
from enum import Enum
import inspect
import random
import time
from aiimages import AIImages
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

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
        
    dirs = Utility.Share.MudDirections()
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
