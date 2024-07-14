import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Hide(Utility):
    logger = None
    command = "hide[hid,h], hide[hid,h] <item>, stash[st,s] <item>"
    examples = ["hide - hide yourself", "hide sword - hide an item", "stash coin - same as hide"]
    description = "Hide yourself or an item in the room."
    type = Utility.Share.Commands.HIDE
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Hide() class", self.logger)

    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1]
        found_item = False

        # check if it's in our inventory
        item_obj = None
        for item_in_inv in player.items.inventory:
            if wanted_item.lower() == item_in_inv.name.lower():
                item_obj = item_in_inv
                found_item = True
                break

        if found_item == True:
            # remove from inventory
            player.inventory.items.remove(item_obj)
            await self.send_message(MudEvents.InfoEvent(f"You hid {item_obj.name}."), player.websocket)
            world_state.rooms.rooms[player.room.id].hidden_items.append(item_obj)
        else:
            await self.send_message(MudEvents.ErrorEvent(f"You aren't carrying {wanted_item} to hide."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        
        return player