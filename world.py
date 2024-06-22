from enum import Enum
import inspect
from environments import Environments
from mudevent import MudEvents
from players import Players
from monsters import Monsters
from utility import Utility
from log_utils import LogUtils
from commands import Commands
from world_events import WorldEvents

class World(Utility):
    world_events = None
    logger = None
    commands = None
    players = None
    monsters = None
    shutdown = False
    weather = None
    world_name = None
    environments = None

    def __init__(self, world_name, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing World() class", self.logger)
        self.world_name = world_name
        LogUtils.info(f"{method_name}: Welcome to NehsaMUD.  {world_name} starting!", self.logger)
        
        if self.world_events is None:
            self.world_events = WorldEvents(self.logger)
          
        if self.commands is None:
            self.commands = Commands(self.logger)

        if self.environments is None:
            self.environments = Environments(self.logger)
            
        if self.players is None:
            self.players = Players(self.logger)

        if self.monsters is None:
            self.monsters = Monsters(self.logger)

    async def alert_world(self, message, world, exclude_player=True, player = None, event_type=MudEvents.InfoEvent):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, message: {message}", self.logger)
        for p in world.players.players:
            if exclude_player and player is not None:
                if p.name != player.name:
                    await self.send_message(event_type(message), p.websocket)
            else:
                await self.send_message(MudEvents.InfoEvent(message), p.websocket)
                
        LogUtils.debug(f"{method_name}: exit", self.logger)

