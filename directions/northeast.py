from log_utils import LogUtils
from utility import Utility

class NorthEast:
    logger = None
    variations = ["ne", "northeast", "northe"]
    opposite = None
    name = "Northeast"
    type = Utility.MudDirections.NORTHEAST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.SOUTHWEST
        LogUtils.debug("Initializing NorthEast() class", self.logger)
