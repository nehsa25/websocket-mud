import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Rogue(PlayerClass):
    logger = None
    name = "Rogue"
    description = "A rogue who can deal damage and evade attacks."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Rogue() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Rogue...", self.logger)
        