import inspect
import random
from log_utils import LogUtils
from mob import Mob
from money import Money
from utility import Utility




class Rite(Mob):
    logger = None
    name = "Rite"
    pronoun = "it"
    type = Utility.Share.Monsters.RITE
    alignment = Utility.Share.Alignment.GOOD
    description = "A small azure and beige colored lizard two feet tall. It looks at you with adorable eyes."
    possible_adjectives = ["Joyful", "Happy"]
    adjective_chance = 20 # chance we'll get something like Nasty
    respawn_rate_secs = None
    dead_epoch = None
    wander = True
    wander_speed = 1  # 1 room / minute
    hitpoints = 10
    damage_potential = "1d4"
    experience = 20
    money = Money(0)
    allowed_in_city = True

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Rite() class", self.logger)
        if random.randint(1, 100) < self.adjective_chance:
            self.name = f"{random.choice(self.possible_adjectives)} Rite"
        self.death_cry = f"{self.name} falls over and dies.."
        self.entrance_cry = f"{self.name} wanders in.."
        self.victory_cry = f"The {self.name} makes no emotion."

        
    def generate(self):
        LogUtils.debug("Generating a Ghoul...", self.logger)