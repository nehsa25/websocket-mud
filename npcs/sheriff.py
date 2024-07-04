import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Sheriff(NpcMob):
    logger = None
    name = "Cog"
    title = "Sheriff"
    description = """The sheriff of Town Smee. The sheriff is a slender, man with a mustache. 
        The sheriff is wearing an unsightly but practical bear cloak across his shoulders to stave off the rain. 
        He has a menacing cudgel at his waist and smiles showing oddly white teeth when he notices you look at it."""
    common_phrases = ["Citizen."]
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "maintaining control", "intimidation", "investigation", "justice"]
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Sheriff() class", self.logger)

    def generate(self):
        LogUtils.info(f"Generating Sheriff {self.name}...", self.logger)