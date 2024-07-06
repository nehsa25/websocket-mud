import asyncio
import inspect
import random
from log_utils import LogUtils
from utility import Utility

class NpcMob(Utility):
    name = ""
    title=""
    description=""
    common_phrases = []
    interests = []
    schedules = []
    wander_event = None
    last_direction = None
    wanders = False
    room = None
    previous_room = None
    
    def __init__(self, logger, name="", description="", title=""):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Npc() class", logger)
        if name == "":
            self.name = self.generate_name(include_identifier=False)
        else:
            self.name = name
            
        self.title = title
        self.description = description
        
    def get_full_name(self):
        return f"{self.title} {self.name}".strip()

    def generate(self):
        LogUtils.info(f"Generating Npc {self.name}...", self.logger)
        return self
    
    # responsible for moving npc
    async def wander(self, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if not self.wanders:
            LogUtils.info(f"{method_name}: {self.name} - I don't wander", self.logger)
            return
        
        LogUtils.info(f"NPC {self.name} wandering!", self.logger)
        
        # get random direction
        direction = None
        if self.last_direction is None:
            direction = random.choice(self.room.exits)
        else:
            found_direction = False
            while not found_direction:
                direction = random.choice(self.room.exits)
                if direction != self.last_direction or len(self.room.exits) == 1:
                    found_direction = True

        await self.move(direction, world_state)
        self.last_direction = direction
            
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return world_state
    
    async def move(self, direction, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        LogUtils.info(f"{method_name}: {self.name} is moving {direction}", self.logger)
        room_id = [a for a in self.room.exits if a["direction"] == direction["direction"]][0]["id"]
        await world_state.move_room_npc(room_id, self, direction)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return world_state
        