import inspect
from log_utils import LogUtils
from utility import Utility


class Statuses(Utility):
    logger = None
    is_dead = None
    is_resting = None
    is_posioned = None
    is_thirsty = False
    is_hungry = False
    mood = Utility.Mood.NORMAL
    posioned = False
    logger = None

    def __init__(self, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing status() class", logger)
        self.is_dead = False
        self.is_resting = False
        self.is_posioned = False
        self.is_thirsty = False
        self.is_hungry = False
        self.mood = Utility.Mood.NORMAL
