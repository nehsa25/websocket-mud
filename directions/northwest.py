from log_utils import LogUtils
from utility import Utility

class NorthWest:
    logger = None
    variations = ["nw", "northwest", "northw"]
    opposite = None
    name = "Northwest"
    type = Utility.MudDirections.NORTHWEST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.SOUTHEAST
        LogUtils.debug("Initializing NorthWest() class", self.logger)
