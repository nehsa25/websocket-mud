import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Maximus(Mob):
    logger = None
    name = "Maximus"
    wanders = True
    description = """Maximus is a overweight orange tabby cat with a white belly and paws.  He has a small white patch on his nose and a long tail.  He is friendly and will often follow you around and rub against your legs."""
    interests = [f"I only exist in the fantasy world of {Utility.WORLD_NAME}, in the town Smee", "cat treats", "cat foot"]
    type = Utility.Npcs.MAXIMUS
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Maximus() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)

    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        
