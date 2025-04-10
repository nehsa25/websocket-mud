import inspect
from log_utils import LogUtils
from mob import Mob
from utility import Utility

class InnKeeper(Mob):
    logger = None
    name = "Jared"
    title = "Innkeeper"
    description = """A slightly obese man with short blonde hair and a sickly pale face. 
        Jared is well beloved by the residents of town Smee, for his charming stories and friendly demeaner. 
        Jared is wearing a lime green button up shirt, old grey breeches with red patches, and a clean white apron. 
        Jared smiles at you welcomely when you look at him."""
    interests = [f"I only exist in the fantasy world of {Utility.WORLD_NAME}, in the town Smee", "cleaing", "checking on guests"]
    type = Utility.Npcs.INNKEEPER

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing InnKeeper() class", self.logger)
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.info(f"Generating {self.type} {self.name} at room {room_id}...", self.logger)
        self.room_id = room_id
        return self
        