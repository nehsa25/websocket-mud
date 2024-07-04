import asyncio
from copy import deepcopy
import inspect
import random
import time
from aiimages import AIImages
from log_utils import LogUtils
from map import Map
from monster import Monster
from townsmee import TownSmee
from utility import Utility


class Environments(Utility):
    monster = None
    running_image_threads = []
    running_map_threads = []
    logger = None
    townsmee = None
    graveyard = None
    forest = None
    jungle = None
    breach = None
    beach = None
    all_rooms = []

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Environments() class", self.logger)

        if self.monster is None:
            self.monster = Monster(self.logger)

        if self.townsmee is None:
            self.townsmee = TownSmee(self.logger)
            self.all_rooms.extend(self.townsmee.rooms)


        # add in npcs
        LogUtils.info(
            f"{method_name}: The world has {len(self.all_rooms)} rooms", self.logger
        )
        
