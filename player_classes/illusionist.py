import inspect
from log_utils import LogUtils
from player_classes.player_class import PlayerClass

class Illusionist(PlayerClass):
    logger = None
    name = "Illusionist"
    description = "An illusionist can create illusions and deceive enemies."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Illusionist() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Illusionist...", self.logger)
        