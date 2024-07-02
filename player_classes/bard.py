import inspect
from log_utils import LogUtils
from utility import Utility


class Bard(Utility):
    logger = None
    name = "Bard"
    description = "A bard who can play music and cast spells to help their allies in battle."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Bard() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Bard...", self.logger)
        