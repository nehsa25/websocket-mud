import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Warlock(PlayerClass):
    logger = None
    name = "Warlock"
    description = "A warlock who can cast spells."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Warlock() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Warlock...", self.logger)
        