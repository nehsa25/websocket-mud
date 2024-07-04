import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Blacksmith(NpcMob):
    logger = None
    name = "Frederick"
    title = "Blacksmith"
    description = """Frederick is a large, balding man despite only just becoming an adult. He has serious Azure eyes and a oiled mustache. 
        Frederick is wearing a leather apron, a leather vest, and leather glove that reach past his elbows."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "metals", "weapons", "armor", "blacksmithing"]

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Blacksmith() class", self.logger)

    def generate(self):
        LogUtils.info(f"Generating Blacksmith {self.name}...", self.logger)