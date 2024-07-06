from log_utils import LogUtils
from utility import Utility

class Down:
    logger = None
    variations = ["d", "dow", "down"]
    opposite = None
    name = "Down"
    type = Utility.Share.MudDirections.DOWN
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.Share.MudDirections.UP
        LogUtils.debug("Initializing Down() class", self.logger)
