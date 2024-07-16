import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Blacksmith(Mob):
    logger = None
    name = "Frederick"
    title = "Blacksmith"
    description = """Frederick is a large, balding man despite only just becoming an adult. He has serious Azure eyes and a oiled mustache. 
        Frederick is wearing a leather apron, a leather vest, and leather glove that reach past his elbows."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "metals", "weapons", "armor", "blacksmithing"]
    type = Utility.Share.Npcs.BLACKSMITH

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Blacksmith() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        