import inspect
from log_utils import LogUtils
from utility import Utility


class Human(Utility):
    logger = None
    name = "Human"
    description = "You. I assume."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Human() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Human...", self.logger)
        