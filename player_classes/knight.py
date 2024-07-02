import inspect
from log_utils import LogUtils
from utility import Utility


class Knight(Utility):
    logger = None
    name = "Knight"
    description = "A knight is a heavily armored warrior who can deal massive damage."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Knight() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Knight...", self.logger)
        