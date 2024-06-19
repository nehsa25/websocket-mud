import inspect
import random
import time
from enum import Enum

from log_utils import LogUtils
from utility import Utility


# how much damage, how fast, ect
class BaseStats(Utility):
    hp = 50
    strength = 3  # 0 - 30
    agility = 3  # 0 - 30
    location = 0
    perception = 50

    def __init__(self, logutils):
        self.logutils = logutils


class CombatTypes(Enum):
    melee = 0
    ranged = 1
    magic = 2


class UnitTypes(Utility):
    logger = None
    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.info("Initializing UnitTypes() class", self.logger)

    class NPC(BaseStats, Utility):
        logger = None
        def __init__(self, logger):
            self.logger = logger
            LogUtils.info("Initializing NPC() class", self.logger)

    class Monster(BaseStats, Utility):
        logger = None
        def __init__(self, logger):
            LogUtils.info("Initializing Monster() class", self.logger)


class Unit(UnitTypes, Utility):
    name = None
    description = None
    type = None
    hp = None
    strength = None
    agility = None
    perception = None
    logger = None

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Unit() class", self.logger)

    def generate_unit(
        self, title, name, hp, strength, agility, perception, description
    ):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.name = name
        self.title = title
        self.hp = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.description = description
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return self

    # uses speed of unit
    # executor.submit(self.ut.move_unit_over_time, self.pgu, self.grid, army_unit, mouse_pos[0], mouse_pos[1]))
    def move_unit_over_time(self, path):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        previousStep = None
        default_speed = 0.35  # higher is faster?
        speed = default_speed - (self.type.speed * 0.1)
        for step in path:
            LogUtils.debug(
                f"Sleeping: {round(speed, 2)} seconds before moving {self.name} again ({self})"
            )
            time.sleep(speed)
            if previousStep is None:
                LogUtils.debug(
                    f"{self.name} beginning travel to {path[len(path)-1]})"
                )
            else:
                LogUtils.debug(
                    f"Moving {self.name} from {previousStep} to {step}"
                )
            previousStep = step
        self.RectSettings.Rect = previousStep
        self.move_thread = False        
        LogUtils.debug(f"{method_name}: exit", self.logger)
