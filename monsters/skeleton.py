import inspect
import random
from log_utils import LogUtils
from mob import Mob
from money import Money
from utility import Utility

class Skeleton(Mob):
    logger = None
    name = "Skeleton"
    pronoun = "it"
    type = Utility.Monsters.SKELETON
    alignment = Utility.Alignment.NEUTRAL
    description = "A dusty old skeleton"
    possible_adjectives = ["Tottering", "Nasty", "Ravaged", "Rotting", "Dapper"]
    adjective_chance = 70 # chance we'll get something like Nasty
    respawn_rate_secs = None
    dead_epoch = None
    wanders = True
    hitpoints = 10
    damage_potential = "1d4"
    experience = 100
        
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Skeleton() class", self.logger)
        if random.randint(1, 100) < self.adjective_chance:
            self.name = f"{random.choice(self.possible_adjectives)} Skeleton"
        self.death_cry = f"{self.name} falls over and dies.."
        self.entrance_cry = f"A {self.name} wanders in.."
        self.victory_cry = f"The {self.name} gives an elegent bow before losing interest."
        self.money = Money(random.randint(0, 10))
        super().__init__(name=self.name, title=self.title, description=self.description, logger=self.logger)
        
    def generate(self, room_id):
        LogUtils.debug("Generating a Skeleton...", self.logger)
        self.room_id = room_id