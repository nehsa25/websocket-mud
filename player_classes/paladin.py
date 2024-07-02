import inspect
from log_utils import LogUtils
from utility import Utility


class Paladin(Utility):
    logger = None
    name = "Paladin"
    description = "A paladin who can heal and deal damage."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Paladin() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Paladin...", self.logger)
        