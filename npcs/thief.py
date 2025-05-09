import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Thief(Mob):
    logger = None
    name = "Tijer"
    title = "Butcher"
    wanders = True
    description = """Tijer the butcher is a tall, thin teenanger. He is wearing a simple tunic and a pair of brown trousers."""
    interests = [f"I only exist in the fantasy world of {Utility.WORLD_NAME}, in the town Smee", "items of value", "valuables", "money", "I have a crush on Princess Candie but I won't tell anyone", "I secretly think you smell like chicken soup and wonder what cannibalism is like"]
    type = Utility.Npcs.THIEF
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Thief() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        