import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Guard(NpcMob):
    logger = None
    name = "" # alas, guards are generic
    title = "Guard"
    description = """The guard stands alert. While in it's armor, you cannot tell many other details. The armour is standard issue but well-maintained hardened leather with metal plating."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "justice", "women", "cards"]

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Guard() class", self.logger)
        
        super().__init__(title=self.title, description=self.description, logger=self.logger)

    def generate(self):
        LogUtils.info(f"Generating Guard {self.name}...", self.logger)