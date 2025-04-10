from log_utils import LogUtils
from utility import Utility

class Up:
    logger = None
    variations = ["u", "up"]
    opposite = None
    name = "Up"
    type = Utility.MudDirections.UP
    def __init__(self, logger):
        self.logger = logger
        self.opposite = Utility.MudDirections.DOWN
        LogUtils.debug("Initializing Up() class", self.logger)
