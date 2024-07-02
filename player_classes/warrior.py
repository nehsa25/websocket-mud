import inspect
from log_utils import LogUtils
from utility import Utility


class Warrior(Utility):
    logger = None
    name = "Warrior"
    description = "A strong and powerful warrior who can take a lot of damage and deal a lot of damage."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Warrior() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Warrior...", self.logger)
        