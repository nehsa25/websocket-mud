import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Armorer(NpcMob):
    logger = None
    name = "Geoff"
    title = "Armorer"
    description = """Geoff is a large, blond haired behemoth of a man. 
        He's nearly 8 feet tall with limbs the size of tree trunks. 
        He wears scalemail armor and looks ready for battle at any moment."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "armor", "weapons", "tools"]
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Armorer() class", self.logger)
        super().__init__(title=self.title, description=self.description, logger=self.logger)

    def generate(self):
        LogUtils.info(f"Generating Armorer {self.name}...", self.logger)