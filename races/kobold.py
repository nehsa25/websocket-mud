import inspect
from log_utils import LogUtils
from unit import BaseStats
from utility import Utility


class Kobold(BaseStats):
    logger = None
    name = "Kobold"
    description = "A small, humanoid creature.  Kobolds are known for their cunning and agility."
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Kobold() class", self.logger)
        
    def generate(self):
        LogUtils.debug("Generating a Kobold...", self.logger)
        