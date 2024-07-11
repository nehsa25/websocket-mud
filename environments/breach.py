import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class Breach:
    monsters = None
    logger = None
    units = None
    in_town = False
    name = "The Breach"
    type = Utility.Share.EnvironmentTypes.BREACH

    # rooms
    breach_portal = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Breach() class", self.logger)
        self.monster_saturation = 2.7
        self.breach_portal = Room(
            name=f"{self.name} - Blue Portal",
            inside=False,
            description="An alien portal stands before you.  It is a shimmering blue, and you can see the other side, shallow water as far as you can see, slow lapping water against a backdrop of several moons. It's unnaturally dark.",
            environment=self.type,
            logger=logger,
        )
