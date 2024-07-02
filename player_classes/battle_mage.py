import inspect
from log_utils import LogUtils
from utility import Utility


class BattleMage(Utility):
    logger = None
    name = "Battle Mage"
    description = "A mage who can cast spells and fight in battle."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing BattleMage() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a BattleMage...", self.logger)
        