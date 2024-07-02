import inspect
from log_utils import LogUtils
from utility import Utility


class Bowman(Utility):
    logger = None
    name = "Bowman"
    description = "A skilled archer who can shoot arrows from a distance."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Bowman() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Bowman...", self.logger)
        