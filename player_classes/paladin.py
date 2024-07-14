import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Paladin(PlayerClass):
    logger = None
    name = "Paladin"
    description = "A paladin who can heal and deal damage."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Paladin() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Paladin...", self.logger)
        