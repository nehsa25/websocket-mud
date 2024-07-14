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
    name = "Green Woods"
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
            description="You are in the great Green Woods forest. Small forest animals and birds are everywhere. Tall but dispersed fir trees spread out around you in all directions. Dry sticks snap and rustle and you walk. It's peaceful and you feel safe.",
            environment=self.type,
            logger=logger,
        )
