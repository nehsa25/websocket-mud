import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class Wizard(NpcMob):
    logger = None
    name = "Renkath"
    title = "Wizard"
    description = """The wizard of Town Smee. The wizard is powerfully built man with a foreboding beard and bald head.  Despite this, he emanates kindness when he notices you!"""
    common_phrases = ["Hello, I am Renkath the wizard.", "I am the wizard of Town Smee."]
    interests = [f"spells", "magic", "omens", "weather", "computer", "programming", "web design"]
    type = Utility.Share.Npcs.WIZARD
    wanders = True
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Wizard() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        