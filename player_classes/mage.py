import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Mage(PlayerClass):
    logger = None
    name = "Mage"
    description = "A mage who can cast spells."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Mage() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Mage...", self.logger)
        