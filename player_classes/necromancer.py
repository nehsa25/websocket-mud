import inspect
from log_utils import LogUtils
from utility import Utility


class Necromancer(Utility):
    logger = None
    name = "Necromancer"
    description = "A necromancer who can raise the dead."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Necromancer() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Necromancer...", self.logger)
        