import inspect
from log_utils import LogUtils
from utility import Utility


class Thief(Utility):
    logger = None
    name = "Thief"
    description = "A weak fighter but can steal items."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Thief() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Thief...", self.logger)
        