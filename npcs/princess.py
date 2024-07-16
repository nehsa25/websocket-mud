import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Princess(Mob):
    logger = None
    name = "Candie"
    title = "Princess"
    wanders = True
    description = """Princess Candie is visiting nobility from a neighboring kingdom to the distant west, across the Tarth sea. She is striking in a shimmering maroon gown."""
    common_phrases = ["Oy vey.", "Hippity Hopper!"]
    interests = [f"I live in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "I can break the fourth wall and talk about game of thrones"]
    type = Utility.Share.Npcs.PRINCESS
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Princess() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        