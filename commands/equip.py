import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Equip(Utility):
    logger = None
    description = "Equip an item from your inventory."
    command = "eq[wield] <target>"
    examples = []
    type = Utility.Share.Commands.EQUIP
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Equip() class", self.logger)
        
    async def execute(self, command, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1]
        found_item = None

        # check if the item is in our inventory
        for item in player.inventory.items:
            if item.name.lower() == wanted_item.lower():
                await self.send_message(MudEvents.InfoEvent(f"You equip {item.name}."), player.websocket)
                item.equiped = True
                found_item = True
                found_item = item

        # if you eq'd an item, deselect any previous items
        for item in player.inventory.items:
            if (
                found_item.item_type == item.item_type and item.equiped == True
            ) and found_item.name != item.name:
                await self.send_message(f"You unequip {item.name}.", "info", player.websocket)
                item.equiped = False
        if found_item == None:
            await self.send_message(f"You cannot equip {wanted_item}.", "error", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
    