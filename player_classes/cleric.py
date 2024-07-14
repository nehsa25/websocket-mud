import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Cleric(PlayerClass):
    logger = None
    name = "Cleric"
    description = "A healer who can heal and buff allies."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Cleric() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Cleric...", self.logger)
        