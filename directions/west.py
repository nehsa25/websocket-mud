from log_utils import LogUtils
from utility import Utility

class West:
    logger = None
    variations = ["w", "west", "wes", "we"]
    opposite = None
    name = "West"
    type = Utility.MudDirections.WEST
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.EAST
        LogUtils.debug("Initializing West() class", self.logger)
