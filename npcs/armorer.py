import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Armorer(Mob):
    logger = None
    name = "Geoff"
    title = "Armorer"
    description = """Geoff is a large, blond haired behemoth of a man. 
        He's nearly 8 feet tall with limbs the size of tree trunks. 
        He wears scalemail armor and looks ready for battle at any moment."""
    interests = [f"I only exist in the fantasy world of {Utility.WORLD_NAME}, in the town Smee", "armor", "weapons", "tools"]
    type = Utility.Npcs.ARMORER
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Armorer() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)

    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
    