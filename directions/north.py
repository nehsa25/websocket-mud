from log_utils import LogUtils
from utility import Utility

class North:
    logger = None
    variations = ["n", "north", "nor"]
    opposite = None
    name = "North"
    type = Utility.MudDirections.NORTH
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.SOUTH
        LogUtils.debug("Initializing North() class", self.logger)
