import inspect
from log_utils import LogUtils
from utility import Utility


class Goblin(Utility):
    logger = None
    name = "Goblin"
    description = "A green, diminutive goblin.  Goblins are known for their stealth and cunning."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Goblin() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a goblin...", self.logger)