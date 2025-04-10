import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class Beach:
    monsters = None
    logger = None
    units = None
    in_town = False
    name = "Black Sands"
    type = Utility.EnvironmentTypes.BEACH

    # rooms
    beach_entry = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Beach() class", self.logger)
        self.monster_saturation = 1
        self.beach_entry = Room(
            name=f"{self.name} - Beach",
            inside=False,
            description="A beach of obsidian black sand stretches out before you.  The sand is hot under a bright sun. The ocean is a deep green, and the waves are crashing against the shore.  The air is filled with the sound of seagulls, bickering crabs, and the smell of salt undertones of decay.",
            environment=self.type,
            logger=logger,
        )
