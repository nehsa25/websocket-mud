import inspect
from log_utils import LogUtils
from utility import Utility


class Arguna(Utility):
    logger = None
    name = "Arguna"
    description = "A big lumbering race. You're slow but strong and hard to kill"
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Arguna() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a arguna...", self.logger)