import inspect
from utility import Utility
from log_utils import LogUtils
from command import Commands

class World(Utility):
    logger = None
    commands = None
    shutdown = False
    weather = None
    world_events = None
    environments = None
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.info(f"{method_name}: Welcome to NehsaMUD.  {Utility.Share.WORLD_NAME} starting!", self.logger)

        if self.commands is None:
            self.commands = Commands(self.logger)
