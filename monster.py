import asyncio
from enum import Enum
import inspect
import random
import time
from random import randint
from log_utils import LogUtils
from money import Money
from monsters.ghoul import Ghoul
from monsters.rite import Rite
from monsters.shade import Shade
from monsters.skeleton import Skeleton
from monsters.wight import Wight
from monsters.wraith import Wraith
from monsters.zombie import Zombie
from monsters.zombie_surfer import ZombieSurfer
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
    
    def get_monster(self, monster_type):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        monster = None
        if monster_type == Utility.Share.Monsters.SKELETON:
            monster = Skeleton(self.logger)
        if monster_type == Utility.Share.Monsters.WIGHT:
            monster = Wight(self.logger)
        if monster_type == Utility.Share.Monsters.GHOUL:
            monster = Ghoul(self.logger)
        if monster_type == Utility.Share.Monsters.SHADE:
            monster = Shade(self.logger)
        if monster_type == Utility.Share.Monsters.WRAITH:
            monster = Wraith(self.logger)
        if monster_type == Utility.Share.Monsters.ZOMBIE:
            monster = Zombie(self.logger)
        if monster_type == Utility.Share.Monsters.ZOMBIE_SURFER:
            monster = ZombieSurfer(self.logger)
        if monster_type == Utility.Share.Monsters.RITE:
            monster = Rite(self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return monster
