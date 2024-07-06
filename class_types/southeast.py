from log_utils import LogUtils
from utility import Utility

class SouthEast:
    logger = None
    variations = ["se", "southeast", "southe"]
    opposite = None
    name = "SouthEast"
    type = Utility.Share.MudDirections.SOUTHEAST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.Share.MudDirections.NORTHWEST
        LogUtils.debug("Initializing SouthEast() class", self.logger)
