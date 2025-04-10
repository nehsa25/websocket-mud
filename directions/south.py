from log_utils import LogUtils
from utility import Utility

class South:
    logger = None
    variations = ["s", "south", "sou"]
    opposite = None
    name = "South"
    type = Utility.MudDirections.SOUTH
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.NORTH
        LogUtils.debug("Initializing South() class", self.logger)
