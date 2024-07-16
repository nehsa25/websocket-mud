import inspect
import random
from log_utils import LogUtils
from mob import Mob
from money import Money
from utility import Utility




class Shade(Mob):
    logger = None
    name = "Shade"
    pronoun = "it"
    type = Utility.Share.Monsters.SHADE
    alignment = Utility.Share.Alignment.NEUTRAL
    description = "A shade"
    possible_adjectives = ["Floating"]
    adjective_chance = 70 # chance we'll get something like Nasty
    respawn_rate_secs = None
    dead_epoch = None
    wanders = True
    hitpoints = 10
    damage_potential = "1d10"
    experience = 250
    money = Money(random.randint(10, 25))
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Shade() class", self.logger)
        if random.randint(1, 100) < self.adjective_chance:
            self.name = f"{random.choice(self.possible_adjectives)} Shade"
        self.death_cry = f"{self.name} falls over and dies.."
        self.entrance_cry = f"{self.name} wanders in.."
        self.victory_cry = F"The {self.name} makes no emotion."
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.debug("Generating a Shade...", self.logger)
        self.room_id = room_id