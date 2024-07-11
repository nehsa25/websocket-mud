import inspect
import random
from log_utils import LogUtils
from mob import Mob
from money import Money
from utility import Utility




class Ghoul(Mob):
    logger = None
    name = "Ghoul"
    pronoun = "it"
    type = Utility.Share.Monsters.GHOUL
    alignment = Utility.Share.Alignment.NEUTRAL
    description = "A eerie ghoul"
    possible_adjectives = ["Eerie"]
    adjective_chance = 70 # chance we'll get something like Nasty
    respawn_rate_secs = None
    dead_epoch = None
    wander = True
    wander_speed = 1  # 1 room / minute
    hitpoints = 10
    damage_potential = "1d4"
    experience = 100
    money = Money(random.randint(0, 10))

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Ghoul() class", self.logger)
        if random.randint(1, 100) < self.adjective_chance:
            self.name = f"{random.choice(self.possible_adjectives)} Ghoul"
        self.death_cry = f"{self.name} falls over and dies.."
        self.entrance_cry = f"{self.name} wanders in.."
        self.victory_cry = f"The {self.name} makes no emotion."
        super().__init__(self.logger, alignment=self.alignment)
        
    def generate(self, room_id):
        LogUtils.debug("Generating a Ghoul...", self.logger)
        self.room_id = room_id