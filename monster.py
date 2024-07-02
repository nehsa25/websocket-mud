import asyncio
from enum import Enum
import inspect
import random
import time
from random import randint
from log_utils import LogUtils
from money import Money
from monsters.skeleton import Skeleton
from mudevent import MudEvents
from utility import Utility


class MonsterStats(Utility):
    name = ""
    hitpoints = 0
    damage = None
    experience = 0
    money = None
    is_alive = True
    in_combat = None
    players_seen = None
    num_attack_targets = None
    respawn_rate_secs = None
    dead_epoch = None
    death_cry = None
    entrance_cry = None
    victory_cry = None
    monster_type = None
    alignment = None
    wander = True
    wander_speed = 1  # 1 room / minute
    pronoun = "it"
    logger = None
    monster_wander_event = None
    last_exit = None
    respawn_rate_secs = 60 * 5

class Monster(Utility):
    logger = None
    skeleton = None
    monsters = []
    
    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Monster() class", self.logger)
        self.skeleton = Skeleton(self.logger)
    
    def get_monster(self, monster_type, worldstate):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        monster = None
        if monster_type == Utility.Share.Monsters.SKELETON:
            monster = Skeleton(self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return monster
    
    # class UndeadFactory:
    #     name = ""
    #     description = "Undead creatures that have been reanimated by dark magic. They are often found in graveyards and other places of death."
    #     font = "comic sans ms"
    #     font_size = 36
    #     log_utils = None

    #     def __init__(self, logger):
    #         self.logger = logger
    #         LogUtils.debug("Initializing undead_factory() class", self.logger)
    #         self.logger = logger



    #     class Skeleton(MonsterStats):
    #         logger = None
            
    #         instance = None

    #         def __init__(self, worldstate, logger):


    #             # create new monster
    #             self.instance = Monster(
    #                 self.name,
    #                 self.hitpoints,
    #                 self.damage_potential,
    #                 self.experience,
    #                 self.money,
    #                 self.death_cry,
    #                 self.entrance_cry,
    #                 self.victory_cry,
                    
    #                 True,
    #                 1,
    #                 "it",
    #                 worldstate,
    #                 self.logger,
    #             )

    #     class Zombie:
    #         possible_adjectives = ["Decrepit", "Rotting", "Mad"]

    #         def __init__(self, room, worldstate, logger):
    #             self.logger = logger
    #             LogUtils.debug("Initializing Zombie() class", logger)
    #             self.name = f"Zombie"
    #             if random.random() < self.adjective_chance:
    #                 self.name = f"{random.choice(self.possible_adjectives)} Zombie"
    #             self.death_cry = f"{self.name} falls over and dies.."
    #             self.entrance_cry = f"{self.name} wanders in.."
    #             self.victory_cry = "The smiles sadly."
    #             self.hitpoints = 12
    #             self.damage_potential = "1d4"
    #             self.experience = 150
    #             self.money = Money(randint(0, 45))

    #     class ZombieSurfer:
    #         adjective_chance = 0.8
    #         possible_adjectives = [
    #             "Wasted",
    #             "Doddering",
    #             "Rotting",
    #             "Scarred",
    #             "Dirty",
    #             "Angry",
    #         ]

    #         def __init__(self, room, worldstate, logger):
    #             self.logger = logger
    #             LogUtils.debug("Initializing ZombieSurfer() class", logger)
    #             self.name = f"Zombie Surfer"
    #             if random.random() < self.adjective_chance:
    #                 self.name = (
    #                     f"{random.choice(self.possible_adjectives)} Zombie Surfer"
    #                 )
    #             self.death_cry = (
    #                 f'{self.name} says "Narley", then falls over and dies..'
    #             )
    #             self.entrance_cry = f"{self.name} wanders in.."
    #             self.victory_cry = (
    #                 "The zombie surfer stares at the corpse in confusion."
    #             )
    #             self.hitpoints = 15
    #             self.damage_potential = "1d6"
    #             self.experience = 175
    #             self.money = Money(randint(0, 50))

    #     class Ghoul:
    #         possible_adjectives = ["Gluttonous", "Scarred", "Ragged"]

    #         def __init__(self, room, worldstate, logger):
    #             self.logger = logger
    #             LogUtils.debug("Initializing Ghoul() class", logger)
    #             self.name = f"Ghoul"
    #             if random.random() < self.adjective_chance:
    #                 self.name = f"{random.choice(self.possible_adjectives)} Ghoul"
    #             self.death_cry = f"{self.name} falls over and dies.."
    #             self.entrance_cry = f"{self.name} wanders in.."
    #             self.victory_cry = "The ghoul makes no emotion."
    #             self.hitpoints = 15
    #             self.damage_potential = "1d6"
    #             self.experience = 175
    #             self.money = Money(randint(0, 75))

    #     class Shade:
    #         alignment = Monster.Alignment.NEUTRAL
    #         possible_adjectives = ["Ethereal", "Dark", "Menacing"]

    #         def __init__(self, room, worldstate, logger):
    #             self.logger = logger
    #             LogUtils.debug("Initializing Shade() class", logger)
    #             self.name = "Shade"
    #             if random.random() < self.adjective_chance:
    #                 self.name = f"{random.choice(self.possible_adjectives)} Share"
    #             self.death_cry = f"{self.name} sighs in relief and fades away.."
    #             self.entrance_cry = f"{self.name} floats in.."
    #             self.victory_cry = "The shade frowns slightly."
    #             self.hitpoints = 45
    #             self.damage_potential = "1d10"
    #             self.experience = 575
    #             self.money = Money(randint(0, 100))

    # logger = None
    # undead = None
    # monsters = []

    # def __init__(self, logger) -> None:
    #     method_name = inspect.currentframe().f_code.co_name
    #     self.logger = logger
    #     LogUtils.debug(f"{method_name}: Initializing Monsters() class", self.logger)
    #     self.undead = self.UndeadFactory(self.logger)
