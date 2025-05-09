import inspect
from log_utils import LogUtils
from utility import Utility


class Attributes(Utility):
    logger = None
    intelligence = 0
    faith = 0
    max_hp = 0
    strength = 0
    agility = 0
    perception = 0
    determination = 0

    def __init__(self, int, faith, agility, perception, determination, strength, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing status() class", logger)
        self.strength = strength
        self.determination = determination
        self.perception = perception
        self.agility = agility
        self.faith = faith
        self.intelligence = int

