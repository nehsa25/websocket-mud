import inspect
from items import Items
from log_utils import LogUtils
from mudevent import HealthEvent, InventoryEvent
from utility import Utility


class Player:
    logger = None
    utility = None
    name = None
    level = 1
    hitpoints = 0
    max_hitpoints = 0
    location = 0
    strength = 0
    agility = 0
    perception = 0
    experience = 0
    resting = False
    in_combat = None
    ip = None
    inventory = [Items.book, Items.cloth_pants]
    money = []
    websocket = None

    def __init__(self, name, hp, strength, agility, location, perception, ip, websocket, logger):
        self.logger = logger
        LogUtils.debug(f"Initializing Player() class", self.logger)
        self.utility = Utility(logger)
        self.name = name
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.location = location
        self.ip = ip
        self.websocket = websocket

    # shows color-coded health bar
    async def show_health(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        msg = f"{self.name}|{str(self.hitpoints)}/{str(self.max_hitpoints)}"
        if self.resting:
            msg += "|REST"            
        health_event = HealthEvent(msg).to_json()
        await self.utility.send_message_raw(health_event, self.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # shows inventory
    async def show_inventory(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        items = []
        for item in self.inventory:
            items.append(item.name)
        inv_event = InventoryEvent(items).to_json()
        await self.utility.send_message_raw(inv_event, self.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
