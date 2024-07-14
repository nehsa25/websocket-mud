import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Get(Utility):
    logger = None
    description = "Get an item from the room floor."
    command = "get[g] <target>"
    examples = []
    type = Utility.Share.Commands.GET
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Get() class", self.logger)
        
    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1].lower()
        found_item = False

        for item in player.room.items:
            if wanted_item == item.name.lower():
                found_item = True
                await self.send_message(MudEvents.InfoEvent(f"You pick up {item.name}."), player.websocket)

                # remove from room
                player.room.items.remove(item)

                # alert the rest of the room
                await player.room.alert(f"{player.name} picks up {item.name}.", exclude_player=True, player=player, event_type=MudEvents.InfoEvent)

                # add to our inventory
                player.inventory.items.append(item)
                break
        if found_item == False:
            await self.send_message(MudEvents.ErrorEvent(f"You cannot find {wanted_item}."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world_state