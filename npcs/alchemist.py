import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Alchemist(Mob):
    logger = None
    name = "Zofia"
    title = "Elder"
    description = """Zofia is a frail old woman. Sit remains seated in her chair and gestures for you to look around and get what you want."""
    interests = [f"I only exist in the fantasy world of {Utility.WORLD_NAME}, in the town Smee", "potions", "herbs", "alchemy", "I am old and tired.", "I am patronizing"]
    type = Utility.Npcs.ALCHEMIST
    
    def __init__(self, room_id, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Alchemist() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)

    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
    