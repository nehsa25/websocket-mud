import inspect
from log_utils import LogUtils
from utility import Utility


class Stats(Utility):
    logger = None
    current_hp = 0
    is_dead = None
    is_resting = None
    is_posioned = None
    feriocity = Utility.Share.Feriocity.NORMAL
    posioned = False
    logger = None
    intelligence = 0
    faith = 0
    max_hp = 0
    strength = 0
    agility = 0
    perception = 0
    determination = 0

    def __init__(self, current_hp, max_hp, int, faith, agility, perception, determination, strength, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing status() class", logger)
        self.strength = strength
        self.determination = determination
        self.perception = perception
        self.agility = agility
        self.faith = faith
        self.intelligence = int
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.is_dead = False
        self.is_resting = False
        self.is_posioned = False
