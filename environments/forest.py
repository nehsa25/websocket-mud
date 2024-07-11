import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class Forest:
    monsters = None
    logger = None
    units = None
    rooms = None
    in_town = False
    name = "Jolly Forest"
    type = Utility.Share.EnvironmentTypes.FOREST

    # rooms
    forest_entry = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Forest() class", self.logger)
        self.monster_saturation = 1.2
        self.forest_entry = Room(
            name=f"{self.name} - Meadow",
            inside=False,
            description="You are in the Jolly forest.  Tall, sparse, fir trees spread out around you in all directions.  Dry sticks snap and rustle and you walk.",
            environment=self.type,
            logger=logger,
        )
