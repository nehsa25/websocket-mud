import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Merchant(NpcMob):
    logger = None
    name = "Roger"
    title = "Merchant"
    description = """Roger, the merchant of Town Smee. Roger is a stout man dressed in fine beige billowing robes. He has a loud high pitched yet friendly voice and is always yelling out to passerby's to come and see his wares."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "money", "buying items", "selling items"]
    type = Utility.Share.Npcs.MERCHANT
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Merchant() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)

    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        
