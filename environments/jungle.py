import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class Jungle:
    monsters = None
    logger = None
    units = None
    rooms = None
    in_town = False
    name = "Jungle"
    type = Utility.EnvironmentTypes.JUNGLE
    exits = None

    # rooms
    jungle_entry = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Jungle() class", self.logger)
        self.monster_saturation = 0.5
        self.jungle_entry = Room(
            name=f"{self.name} - Entrance",
            inside=False,
            description="You are in a densely covered jungle.  Orange and blue trees, thick with grayish underbrush lie everywhere. The air is humid, and the ground is moist. A constant stream of noise assaults you from all directions. Water dripping, birds chirping, insects buzzing around. It's unnaturally dark due to lack of sunlight.",
            environment=self.type,
            logger=logger,
        )
