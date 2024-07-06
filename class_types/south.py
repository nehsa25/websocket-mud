from log_utils import LogUtils
from utility import Utility

class South:
    logger = None
    variations = ["s", "south", "sou"]
    opposite = None
    name = "South"
    type = Utility.Share.MudDirections.SOUTH
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.Share.MudDirections.NORTH
        LogUtils.debug("Initializing South() class", self.logger)
