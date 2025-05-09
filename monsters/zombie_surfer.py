import inspect
import random
from log_utils import LogUtils
from mob import Mob
from money import Money
from utility import Utility

class ZombieSurfer(Mob):
    logger = None
    name = "Zombie Surfer"
    pronoun = "it"
    type = Utility.Monsters.ZOMBIE_SURFER
    alignment = Utility.Alignment.NEUTRAL
    description = "A zombie wearing shorts"
    possible_adjectives = ["Tottering", "Nasty", "Ravaged", "Rotting", "Dapper"]
    adjective_chance = 70 # chance we'll get something like Nasty
    respawn_rate_secs = None
    dead_epoch = None
    wanders = True
    hitpoints = 10
    damage_potential = "1d8"
    experience = 225
    money = Money(random.randint(5, 10))
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing ZombieSurfer() class", self.logger)
        if random.randint(1, 100) < self.adjective_chance:
            self.name = f"{random.choice(self.possible_adjectives)} Zombie Surfer"
        self.death_cry = (
            f'{self.name} says "Narley", then falls over and dies..'
        )
        self.entrance_cry = f"{self.name} wanders in.."
        self.victory_cry = (
            "The zombie surfer stares at the corpse in confusion."
        )
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.debug("Generating a ZombieSurfer...", self.logger)
        self.room_id = room_id