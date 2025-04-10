import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class Gardener(Mob):
    logger = None
    name = "Jaque"
    title = "Gardener"
    description = """The gardener of the University. Jaque is an absolutely tiny boy, no wait, woman. Despite wearing only simple white robes or apparent effort, she emanates both power and grace. She welcomes you with a smile when she notices you. As a strict requirement for gardeners at the University, bright orange headgear and gloves are always worn."""
    common_phrases = ["Hello, I am Jaque the gardener (wink).", "I am the gardener for the University.", "YOU THOUGHT I WAS A BOY DIDN'T YOU?"]
    interests = [f"I only exist in the fantasy world of {Utility.WORLD_NAME}, in the town Smee", "spells", "I am secretly a evil wizard but I don't want anyone to know", "magic", "omens", "weather", "gardening"]
    type = Utility.Npcs.GARDENER
    wanders = False
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Gardener() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        