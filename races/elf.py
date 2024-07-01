import inspect
from log_utils import LogUtils
from utility import Utility


class Elf(Utility):
    logger = None
    name = "Elf"
    description = "A tall, slender elf"
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Elf() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a elf...", self.logger)
        