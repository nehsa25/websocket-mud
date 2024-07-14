import inspect
from log_utils import LogUtils
from utility import Utility

class Inventory(Utility):
    logger = None
    command = "inventory[inv,i]"
    examples = []
    description = "View the items in your inventory."
    type = Utility.Share.Commands.INVENTORY
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Inventory() class", self.logger)

    async def execute(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await player.send_inventory()
        LogUtils.debug(f"{method_name}: exit", self.logger)