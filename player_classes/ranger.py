import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Ranger(PlayerClass):
    logger = None
    name = "Ranger"
    description = "A ranger who can use a bow and speak with animals."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Ranger() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Ranger...", self.logger)
        