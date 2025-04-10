from log_utils import LogUtils
from utility import Utility

class SouthEast:
    logger = None
    variations = ["se", "southeast", "southe"]
    opposite = None
    name = "Southeast"
    type = Utility.MudDirections.SOUTHEAST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.NORTHWEST
        LogUtils.debug("Initializing SouthEast() class", self.logger)
