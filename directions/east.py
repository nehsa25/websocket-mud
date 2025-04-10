from log_utils import LogUtils
from utility import Utility

class East:
    logger = None
    variations = ["e", "east", "eas", "ea"]
    opposite = None
    name = "East"
    type = Utility.MudDirections.EAST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.WEST
        LogUtils.debug("Initializing East() class", self.logger)
