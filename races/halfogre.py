import inspect
from log_utils import LogUtils
from utility import Utility


class HalfOgre(Utility):
    logger = None
    name = "Half-Ogre"
    description = "A large, brutish half-ogre.  Half-ogres are known for their strength and toughness."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing HalfOgre() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a HalfOgre...", self.logger)
        