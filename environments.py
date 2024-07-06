import inspect
from class_types.direction import Directions
from log_utils import LogUtils
from monster import Monster
from townsmee import TownSmee
from utility import Utility


class Environments(Utility):
    monster = None
    running_image_threads = []
    running_map_threads = []
    logger = None
    townsmee = None
    all_rooms = []
    dirs = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Environments() class", self.logger)

        self.dirs = Directions(self.logger)

        if self.monster is None:
            self.monster = Monster(self.logger)

        if self.townsmee is None:
            self.townsmee = TownSmee(self.dirs, self.logger)
            self.all_rooms.extend(self.townsmee.rooms)

        # add in npcs
        LogUtils.info(
            f"{method_name}: The world has {len(self.all_rooms)} rooms", self.logger
        )
