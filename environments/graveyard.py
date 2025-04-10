import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class Graveyard:
    monsters = None
    logger = None
    units = None
    rooms = None
    in_town = False
    name = "Graveyard"
    type = Utility.EnvironmentTypes.GRAVEYARD
    exits = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Graveyard() class", self.logger)
        self.monster_saturation = 1.5
        self.rooms = [
            Room(
                name=f"{self.name} - Entrance",
                inside=False,
                description="You are in a graveyard.  The gravestones are old and crumbling, and the trees are twisted and gnarled.  It's too quiet.",
                environment=self.type,
                logger=logger,
            )
        ]
