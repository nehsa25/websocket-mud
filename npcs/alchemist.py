import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Alchemist(NpcMob):
    logger = None
    name = "Zofia"
    title = "Elder"
    description = """Zofia is a frail old woman. Sit remains seated in her chair and gestures for you to look around and get what you want."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "potions", "herbs", "alchemy", "I am old and tired.", "I am patronizing"]

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Alchemist() class", self.logger)
        super().__init__(title=self.title, description=self.description, logger=self.logger)

    def generate(self):
        LogUtils.info(f"Generating Alchemist {self.name}...", self.logger)