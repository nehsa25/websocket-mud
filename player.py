import asyncio
import inspect
from random import randint
import random
from items import Items
from log_utils import LogUtils
from mudevent import MudEvents
from rooms import Rooms
from utility import Utility

class Player(Utility):
    logger = None
    utility = None
    name = None
    level = 1
    hitpoints = 0
    max_hitpoints = 0
    location_id = 0
    strength = 0
    agility = 0
    perception = 0
    experience = 0
    is_resting = False
    in_combat = None
    weapon = Items.club
    ip = None
    inventory = [Items.club, Items.book, Items.cloth_pants]
    money = []
    websocket = None
    rest_task = None # A resting task that check if this user is resting every 2 seconds
    mob_attack_task = None
    DEATH_RESPAWN_ROOM = 6
    room = None
    previous_room = None

    def __init__(
        self,
        name,
        hp,
        strength,
        agility,
        location_id,
        perception,
        ip,
        websocket,
        logger,
    ):
        self.logger = logger
        LogUtils.debug(f"Initializing Player() class", self.logger)
        self.name = name
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.location_id = location_id
        self.ip = ip
        self.websocket = websocket        
        rooms = Rooms("Illisurom", self.logger)
        
        if self.rest_task is None:
            self.rest_task = asyncio.create_task(self.check_for_resting(rooms))
            
        # if self.mob_attack_task is None:
        #     self.mob_attack_task = asyncio.create_task(self.check_for_new_attacks())

    async def set_rest(self, rest: bool):
        if rest:
            self.send_message(MudEvents.RestEvent("You start resting.", is_resting=True), self.websocket)
            self.is_resting = True
        else:
            if self.is_resting:
                self.is_resting = False
                await self.send_message(MudEvents.RestEvent("You are no longer resting.", is_resting=False), self.websocket)  
            else:
                await self.send_message(MudEvents.InfoEvent("You were not resting to begin with."), self.websocket)  
        
    # shows color-coded health bar
    async def send_health(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        msg = f"{self.name}|{str(self.hitpoints)}/{str(self.max_hitpoints)}"
        await self.send_message(MudEvents.HealthEvent(msg, self.is_resting), self.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # cancels all tasks and states you died if you die
    async def you_died(self, world):
        
        # Your done boy.  Done.
        self.in_combat = False        

        # state you died
        await self.send_message(MudEvents.InfoEvent("You died."), self.websocket)

        # alert others in the room where you died that you died..
        await self.alert_room(f"{self.name} died.", self.room, True, self)

        # drop all items
        for item in self.inventory:
            self.room.items.append(item)
        self.inventory = []

        # set player location to death respawn room
        player, world = await world.rooms.move_room(
            self.DEATH_RESPAWN_ROOM, self, world
        )

        # alert others in the room that new player has arrived
        await self.alert_room(f"A bright purple spark floods your vision.  When it clears, {self.name} is standing before you.  Naked.", player.room, True, self)

        # set hits back to max / force health refresh
        self.hitpoints = self.max_hitpoints
        await self.send_health()
        
        return player, world

    # break combat
    async def break_combat(self, rooms):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.in_combat = None        
        self.alert_room(f"{self.name} stops fighting.", rooms[self.location_id])        
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # shows inventory
    async def send_inventory(self):
        if self.inventory == [] and self.money == []:
            await self.send_message(MudEvents.InventoryEvent("You have nothing in your inventory."), self.websocket)
        else:
            msg = "You have the following items in your inventory:<br>"
            for item in self.inventory:
                if item.equiped == True:
                    msg += f"* {item.name} (Equiped)<br>"
                else:
                    msg += f"* {item.name}<br>"

            # get money
            money = len(self.money)
            if money > 0:
                msg += f"{money} copper<br>"
            else:
                msg += f"You have no money.<br>"
                
            await self.send_message(MudEvents.InventoryEvent(msg), self.websocket)

    # increases hp when resting
    async def check_for_resting(self, rooms):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, checking if {self.name} is resting..", self.logger)

        while True:
            # Check resting every 2 seconds
            await asyncio.sleep(self.REST_WAIT_SECS)

            if self.is_resting == True:
                LogUtils.debug("Checking if resting...", self.logger)
                if self.hitpoints < self.max_hitpoints:
                    heal = randint(1, 3)
                    if heal == 1:
                        await self.send_message(MudEvents.InfoEvent(f"You recover {heal} hitpoint."))
                    else:
                        await self.send_message(MudEvents.InfoEvent(f"You recover {heal} hitpoints."))
                    self.hitpoints += 3
                    if self.hitpoints >= self.max_hitpoints:
                        self.hitpoints = self.max_hitpoints
                        self.set_rest(False)
                        await self.send_message(MudEvents.InfoEvent("You have fully recovered."))
                        await self.alert_room(f"{self.name} appears to have fully recovered.", rooms[self.location_id])
                    await self.send_health()
