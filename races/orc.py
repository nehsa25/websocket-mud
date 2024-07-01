import inspect
from log_utils import LogUtils
from utility import Utility

class Orc(Utility):
    logger = None
    name = "Orc"
    description = "A large, brutish orc.  Orcs are known for their strength and toughness."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Orc() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Orc...", self.logger)
        