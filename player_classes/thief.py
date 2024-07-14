import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Thief(PlayerClass):
    logger = None
    name = "Thief"
    description = "A weak fighter but can steal items."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Thief() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Thief...", self.logger)
        