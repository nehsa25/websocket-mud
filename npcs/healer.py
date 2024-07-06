import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Healer(NpcMob):
    logger = None
    name = "Omar"
    title = "Healer"
    description = """Omar is a slender, average height man with a long red beard. He has a serious demeanor and is always looking at you with a piercing gaze."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "money", "selling items"]
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Healer() class", self.logger)
        super().__init__(title=self.title, description=self.description, logger=self.logger)
        

    def generate(self):
        LogUtils.info(f"Generating Healer {self.name}...", self.logger)