from log_utils import LogUtils
from utility import Utility

class SouthWest:
    logger = None
    variations = ["sw", "southwest", "southw"]
    opposite = None
    name = "Southwest"
    type = Utility.Share.MudDirections.SOUTHWEST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.Share.MudDirections.NORTHEAST
        LogUtils.debug("Initializing SouthWest() class", self.logger)
