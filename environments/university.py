import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class University:
    monsters = None
    logger = None
    units = None
    rooms = None
    in_town = True
    name = "Town Smee - University"
    type = Utility.Share.EnvironmentTypes.UNIVERSITY
    
    # rooms
    university_entry = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing University() class", self.logger)
        self.monster_saturation = 0.5
        self.university_entry = Room(
                name=f"{self.name} - Entrance Stone Arches",
                inside=False,
                description="The university is a sprawling complex of buildings, courtyards, and gardens. The buildings are made of a white stone that seems to glow in the sunlight. The university is a place of learning and research. The air is filled with the sounds of students and teachers going about their business. The university is a place of peace and tranquility.",
                environment=self.type,
                logger=logger
            )
        