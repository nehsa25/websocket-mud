from log_utils import LogUtils
from utility import Utility

class NorthWest:
    logger = None
    variations = ["nw", "northwest", "northw"]
    opposite = None
    name = "Northwest"
    type = Utility.Share.MudDirections.NORTHWEST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.Share.MudDirections.SOUTHEAST
        LogUtils.debug("Initializing NorthWest() class", self.logger)
