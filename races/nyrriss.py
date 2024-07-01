import inspect
from log_utils import LogUtils
from utility import Utility


class Nyrriss(Utility):
    logger = None
    name = "Nyrriss"
    description = "A citizen from the swamps of Nyrriss"
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Nyrriss() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Nyrriss...", self.logger)
        