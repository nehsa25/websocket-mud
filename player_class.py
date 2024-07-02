
from log_utils import LogUtils
from player_classes.barbarian import Barbarian
from player_classes.bard import Bard
from player_classes.battle_mage import BattleMage
from player_classes.berserker import Berserker
from player_classes.bowman import Bowman
from player_classes.cleric import Cleric
from player_classes.druid import Druid
from player_classes.illusionist import Illusionist
from player_classes.knight import Knight
from player_classes.mage import Mage
from player_classes.monk import Monk
from player_classes.necromancer import Necromancer
from player_classes.paladin import Paladin
from player_classes.ranger import Ranger
from player_classes.rogue import Rogue
from player_classes.sorcerer import Sorcorer
from player_classes.thief import Thief
from player_classes.warlock import Warlock
from player_classes.warrior import Warrior


class Class:
    logger = None
    warrior = None
    Mage = None
    thief = None
    cleric = None
    ranger = None
    druid = None
    bard = None
    paladin = None
    monk = None
    barbarian = None
    warlock = None
    sorcerer = None
    rogue = None
    berserker = None
    battle_mage = None
    bowman = None
    knight = None
    necromancer = None
    illusionist = None

    def __init__(
        self, logger
    ):
        self.logger = logger
        LogUtils.debug("Initializing Class() class", self.logger)
        
        self.warrior = Warrior(self.logger)
        self.mage = Mage(self.logger)
        self.thief = Thief(self.logger)
        self.cleric = Cleric(self.logger)
        self.barbarian = Barbarian(self.logger)
        self.bard = Bard(self.logger)
        self.berserker = Berserker(self.logger)
        self.bowman = Bowman(self.logger)
        self.druid = Druid(self.logger)
        self.illusionist = Illusionist(self.logger)
        self.knight = Knight(self.logger)
        self.monk = Monk(self.logger)
        self.necromancer = Necromancer(self.logger)
        self.paladin = Paladin(self.logger)
        self.ranger = Ranger(self.logger)
        self.rogue = Rogue(self.logger)
        self.sorcerer = Sorcorer(self.logger)
        self.warlock = Warlock(self.logger)
        self.battle_mage = BattleMage(self.logger)
