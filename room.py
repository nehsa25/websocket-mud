import asyncio
from copy import deepcopy
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
        RANDOM = 7  

    name = ""
    inside = False
    description = ""
    monster_spawn = False
    monster_saturation = 0.7
    scariness = 0
    environment = (None,)
    history = []
    exits = ([],)
    items = ([],)
    hidden_items = ([],)
    monsters = ([],)
    players = ([],) # you, hopefully
    npcs = [] # actual instances of npcs
    npc_types = [] # this is the enum of the types of npcs that can be in the room
    in_town = False
    logger = None

    def __init__(
        self,
        name,
        inside,
        description,
        environment,
        logger,
        scariness=None,
        items=[],
        hidden_items=[],
        monsters=[],
        players=[],
        npcs=[],
        npc_types=[],
        in_town=False,
    ) -> None:
        self.name = name
        self.inside = inside
        self.description = description
        self.environment = environment
        self.items = items
        self.scariness = scariness
        self.hidden_items = hidden_items
        self.monsters = monsters
        self.players = players
        self.npcs = npcs
        self.in_town = in_town
        self.npc_types = npc_types
        self.logger = logger
        self.scariness = random.choice(list(self.Scariness)).value
        LogUtils.debug(f"Initializing Room() class", self.logger)

    def set_exits(self, exits):
        self.exits = exits        
        return deepcopy(self)
        
    async def alert(
        self, message, 
        exclude_player=False, 
        player=None, 
        event_type=MudEvents.InfoEvent,
        adjacent_message=""
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
                
        if adjacent_message != "":
            for e in self.exits:
                if e is not None:
                    await e.alert(adjacent_message, event_type=event_type, adjacent=False)
