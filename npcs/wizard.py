import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Wizard(NpcMob):
    logger = None
    name = "Jaque"
    title = "Wizard"
    description = """The wizard of Town Smee. The wizard is an absolutely tiny boy, no wait, woman. Despite wearing only simple white robes or apparent effort, she emanates both power and grace. She welcomes you with a smile when she notices you."""
    common_phrases = ["Hello, I am Jaque the wizard.", "I am the wizard of Town Smee.", "YOU THOUGHT I WAS A BOY DIDN'T YOU?"]
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "spells", "magic", "omens", "weather"]
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Wizard() class", self.logger)
        super().__init__(title=self.title, description=self.description, logger=self.logger)
        
    def generate(self):
        LogUtils.info(f"Generating Wizard {self.name}...", self.logger)
