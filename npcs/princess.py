import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Princess(NpcMob):
    logger = None
    name = "Candie"
    title = "Princess"
    description = """Princess Candie is visiting nobility from a neighboring kingdom to the distant west, across the Tarth sea. She is striking in a shimmering maroon gown."""
    common_phrases = ["Oy vey.", "Hippity Hopper!"]
    interests = [f"I live in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "I can break the fourth wall and talk about game of thrones"]
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Princess() class", self.logger)

    def generate(self):
        LogUtils.info(f"Generating Princess {self.name}...", self.logger)