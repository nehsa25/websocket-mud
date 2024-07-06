import inspect
from log_utils import LogUtils
from npc_mob import NpcMob
from utility import Utility

class InnKeeper(NpcMob):
    logger = None
    name = "Jared"
    title = "Innkeeper"
    description = """A slightly obese man with short blonde hair and a sickly pale face. 
        Jared is well beloved by the residents of town Smee, for his charming stories and friendly demeaner. 
        Jared is wearing a lime green button up shirt, old grey breeches with red patches, and a clean white apron. 
        Jared smiles at you welcomely when you look at him."""
    interests = [f"I only exist in the fantasy world of {Utility.Share.WORLD_NAME}, in the town Smee", "cleaing", "checking on guests"]

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Sheriff() class", self.logger)
        super().__init__(title=self.title, description=self.description, logger=self.logger)
        
    def generate(self):
        LogUtils.info(f"Generating Sheriff {self.name}...", self.logger)