import asyncio
import inspect
import random
import time
from alignment import Alignment
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
    room_id = None
    prev_room_id = None
    last_check_combat = None
    alignment = None
    in_combat = False

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
        self.alignment = Alignment(Utility.Share.Alignment.GOOD, self.logger)
        
    def get_attack_phrase(self, target):    
        npc_attack_templates = [
            f"{self.name} alters course to intercept {target}!",
            f"{self.name} moves to attack {target}!",
            f"{self.name} moves to block {target}'s path!",
        ]
        return random.choice(npc_attack_templates)
    
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
        room = await world_state.get_room(self.room_id)  
        if self.last_direction is None:
            direction = random.choice(room.exits)
        else:
            found_direction = False
            while not found_direction:
                direction = random.choice(room.exits)
                if direction != self.last_direction or len(room.exits) == 1:
                    found_direction = True

        self, world_state = await self.move(direction, world_state)
        self.last_direction = direction
            
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return world_state
    
    # responsible for checking combat
    async def check_combat(self, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        # check for alignments opposite of npc
        room = await world_state.get_room(self.room_id)
        
        if self.in_combat and not len(room.players) > 0:
            return world_state
        
        current_time = time.time()
        if  self.last_check_combat is None:
            self.last_check_combat = current_time
        LogUtils.info(f"{method_name}: Time between combat checks: {current_time - self.last_check_combat}", self.logger)
        

        
        # check players
        for p in room.players:
            if await self.alignment.is_opposing_alignment(p.alignment):
                LogUtils.info(f"{method_name}: {self.name} is attacking {p.name}".upper(), self.logger)
                room.alert(self.get_attack_phrase(p.name))

        # check npcs
        for n in room.npcs:
            if await self.alignment.is_opposing_alignment(n.alignment):
                LogUtils.info(f"{method_name}: {self.name} is attacking {n.name}".upper(), self.logger)
                room.alert(self.get_attack_phrase(n.name))
   
        # check for monsters
        for m in room.monsters:
            if await self.alignment.is_opposing_alignment(m.alignment):                
                LogUtils.info(f"{method_name}: {self.name} is attacking {m.name}".upper(), self.logger)
                if len(room.players) > 0:
                    await room.alert(self.get_attack_phrase(m.name))
            
        self.last_check_combat = current_time
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return world_state
    
    
    async def move(self, direction, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        LogUtils.info(f"{method_name}: {self.name} is moving {direction}", self.logger)
        room = await world_state.get_room(self.room_id)  
        room_id = [a for a in room.exits if a["direction"] == direction["direction"]][0]["id"]
        self, world_state = await world_state.move_room_npc(room_id, self, direction)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return self, world_state
        