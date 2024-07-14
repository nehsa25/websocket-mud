import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Berserker(PlayerClass):
    logger = None
    name = "Berserker"
    description = "Berserkers who can take a lot of damage and deal a lot of damage. Will go berserk in battle."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Berserker() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Berserker...", self.logger)
        