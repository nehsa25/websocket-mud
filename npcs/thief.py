import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Thief(NpcMob):
    logger = None
    name = "Tijer"
    description = """Tijer the butcher is a tall, thin teenanger. He is wearing a simple tunic and a pair of brown trousers."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "items of value"]
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Thief() class", self.logger)

    def generate(self):
        LogUtils.info(f"Generating Thief {self.name}...", self.logger)