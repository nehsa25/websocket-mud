import inspect
from log_utils import LogUtils
from utility import Utility


class Fae(Utility):
    logger = None
    name = "Fae"
    description = "A citizen of the fae realm",
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Fae() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Fae...", self.logger)
        