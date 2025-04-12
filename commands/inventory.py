import inspect
from log_utils import LogUtils
from utility import Utility
from mudevent import MudEvents
from item import Item

class Inventory(Utility):
    logger = None
    command = "inventory"
    examples = [
        "i",
        "inv",
        "inventory",
    ]
    description = "View inventory"
    type = Utility.Commands.INVENTORY

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Inventory() class", self.logger)
        self.items = []  # Initialize the items list here

    async def execute(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await player.send_inventory()
        LogUtils.debug(f"{method_name}: exit", self.logger)
