import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Sorcorer(PlayerClass):
    logger = None
    name = "Sorcorer"
    description = "A sorcorer who can cast spells."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Sorcorer() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Sorcorer...", self.logger)
        