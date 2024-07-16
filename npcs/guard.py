import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Guard(Mob):
    logger = None
    name = "" # alas, guards are generic
    title = "Guard"
    description = """The guard stands alert. While in it's armor, you cannot tell many other details. The armour is standard issue but well-maintained hardened leather with metal plating."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "justice", "women", "cards"]
    wanders = True
    type = Utility.Share.Npcs.GUARD

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Guard() class", self.logger)        
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)

    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self