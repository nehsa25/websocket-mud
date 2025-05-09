import inspect
import random
from log_utils import LogUtils
from mob import Mob
from money import Money
from utility import Utility

class Wight(Mob):
    logger = None
    name = "Wight"
    pronoun = "it"
    type = Utility.Monsters.WIGHT
    alignment = Utility.Alignment.NEUTRAL
    description = "Wights are deceased humans, cursed to endure horrific pain. They look humannoid in appearance but with an odd jerky grace and molton-red eyes."
    possible_adjectives = ["Tottering", "Nasty", "Ravaged", "Rotting", "Dapper"]
    adjective_chance = 70 # chance we'll get something like Nasty
    respawn_rate_secs = None
    dead_epoch = None
    wanders = True
    hitpoints = 10
    damage_potential = "2d12"
    experience = 300
    money = Money(random.randint(0, 10))
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Wight() class", self.logger)
        if random.randint(1, 100) < self.adjective_chance:
            self.name = f"{random.choice(self.possible_adjectives)} Wight"
        self.death_cry = f"{self.name} falls over and dies.."
        self.entrance_cry = f"A {self.name} wanders in.."
        self.victory_cry = f"The {self.name} gives an elegent bow before losing interest."
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.debug("Generating a Wight...", self.logger)
        self.room_id = room_id