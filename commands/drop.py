import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Drop(Utility):
    logger = None
    description = "Drop an item to the ground"
    command = "drop <target>"
    examples = [
        "d sword - drop a sword",
    ]
    type = Utility.Commands.DROP
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Drop() class", self.logger)
        
    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1].lower()
        await player.inventory.drop_item(wanted_item, player)
        LogUtils.debug(f"{method_name}: exit", self.logger)

        return player, world_state