import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Healer(Mob):
    logger = None
    name = "Omar"
    title = "Healer"
    description = """Omar is a slender, average height man with a long red beard. He has a serious demeanor and is always looking at you with a piercing gaze."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "money", "selling items"]
    type = Utility.Share.Npcs.HEALER
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Healer() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
    