import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Monk(PlayerClass):
    logger = None
    name = "Monk"
    description = "A monk who can deal damage and heal."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Monk() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Monk...", self.logger)
        