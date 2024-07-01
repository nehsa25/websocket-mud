import inspect
from log_utils import LogUtils
from utility import Utility


class Earea(Utility):
    logger = None
    name = "Earea"
    description = "Telepathic hive mind creatures. No one knows where or how they came to be"
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Earea() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a earea...", self.logger)
        