from enum import Enum
import inspect
import random
import time
from log_utils import LogUtils
from mudevent import MudEvents

class Utility(MudEvents):
    common_names = [
        "William",
        "Olga",
        "Omar",
        "Jill",
        "Jack",
        "John",
        "Jane",
        "Stefan",
        "Sven",
        "Svetlana",
        "Sergei",
        "Serge",
        "Isabella",
        "Isaac",
        "Ivan",
        "Igor",
        "Vlad",
        "Vladimir",
        "Dimi",
        "Dimitri",
        "Dimitrius",
        "Ali",
        "Alyssa",
        "Alicia",
        "Giles",
        "Gerald",
        "Geraldine",
        "Geoffrey",
        "Tom",
        "Thomas"
    ]
    
    common_sirnames = [
        "Smith",
        "Johnson",
        "Williams",
        "Jones",
        "Brown",
        "Davis",
        "Draper",
        "Chandler"
    ]
    
    common_identifiers = [
        "the Brave",
        "the Cowardly",
        "the Fool",
        "the greedy",
        "the Prideful",
        "the Wise",
        "the Strong",
        "Quickfoot",
        "the Swift",
    ]

    class Share:
        WORLD_NAME = "Illisurom"
        PLAYER_BASE_REST_WAIT_SECS = 2
        EVENT_SPEED = PLAYER_BASE_REST_WAIT_SECS

        class EnvironmentTypes(Enum):
            TOWNSMEE = 1
            BEACH = 2
            FOREST = 3
            JUNGLE = 4
            BREACH = 5
            GRAVEYARD = 6
            UNIVERSITY = 7

        class Races(Enum):
            HUMAN = (0,)
            KOBOLD = (1,)
            GOBLIN = (2,)
            HALFLING = (3,)
            HALFOGRE = (4,)
            ORC = (5,)
            ELF = (6,)
            FAE = (7,)
            NYRRISS = (8,)
            ARGUNA = (9,)
            EAREA = 10

        class Classes(Enum):
            WARRIOR = (0,)
            MAGE = (1,)
            THIEF = (2,)
            CLERIC = (3,)
            RANGER = (4,)
            DRUID = (5,)
            BARD = (6,)
            PALADIN = (7,)
            MONK = (8,)
            BARBARIAN = (9,)
            WARLOCK = (10,)
            SORCERER = (11,)
            ROGUE = (12,)
            BERSERKER = (13,)
            BATTLE_MAGE = (14,)
            BOWMAN = (15,)
            KNIGHT = (16,)
            NECROMANCER = (17,)
            ILLUSIONIST = 18

        class MudDirections(Enum):  # directions
            UP = 0
            DOWN = 1
            NORTH = 2
            SOUTH = 3
            EAST = 4
            WEST = 5
            NORTHWEST = 6
            NORTHEAST = 7
            SOUTHEAST = 8
            SOUTHWEST = 9

        class DayOrNight(Enum):
            DAY = 1
            NIGHT = 2

        class Coin(Enum):
            Copper = 1
            Silver = 2
            Gold = 3

        class ImageType(Enum):
            ROOM = 0
            ITEM = 1
            PLAYER = 2
            NPC = 3
            MONSTER = 4

        # how much is your blood pumping?
        class Feriocity(Enum):
            NORMAL = 1
            MAD = 2
            ENRAGED = 3
            FRENZIED = 4
            BERSERK = 5

        class Monsters(Enum):
            SKELETON = 1
            ZOMBIE = 2
            ZOMBIE_SURFER = 3
            GHOUL = 4
            SHADE = 5
            WIGHT = 6
            WRAITH = 7
            RITE = 8

        class Npcs(Enum):
            SHERIFF = 1
            INNKEEPER = 2
            BLACKSMITH = 3
            ALCHEMIST = 4
            WIZARD = 5
            HEALER = 6
            MERCHANT = 7
            GUARD = 8
            THIEF = 9
            ARMORER = 10
            PRINCESS = 11
            GARDENER = 12

        class Alignment(Enum):
            GOOD = 1  # attacks evil players only
            NEUTRAL = 2  # only attacks if attacked
            EVIL = 3  # attacks good players only
            CHOATIC = 4  # attacks all players

        class WeatherTypes(Enum):
            RAIN = 1
            THUNDER = 2
            SUN = 3
            SNOW = 4
            FOG = 5
            OVERCAST = 6

        class WeatherStrength(Enum):
            LIGHT = 1
            MEDIUM = 2
            HEAVY = 3

        class WeatherSeasons(Enum):
            SPRING = 1
            SUMMER = 2
            FALL = 3
            WINTER = 4

        class AIGeneration(Enum):
            StabilityAI = 1
            GeminiAI = 2

        class EyeColors(Enum):
            BLUE = 1
            GREEN = 2
            BROWN = 3
            HAZEL = 4
            GRAY = 5
            AMBER = 6
            RED = 7
            VIOLET = 8
            BLACK = 9
            WHITE = 10
            SILVER = 11
            GOLD = 12
            AQUA = 13
            TEAL = 14
            ORANGE = 15

        class HairColors(Enum):
            BLACK = 1
            BROWN = 2
            BLONDE = 3
            RED = 4
            GRAY = 5
            WHITE = 6
            SILVER = 7
            BLUE = 8

        class TattooPlacements(Enum):
            FACE = 0
            NECK = 1
            ARM = 2

        class TattooSeverities(Enum):
            NONE = 0
            LIGHT = 1
            MEDIUM = 2
            HEAVY = 3

        class Scars(Enum):
            NONE = 0
            LIGHT = 1
            MEDIUM = 2
            HEAVY = 3
            SEVERE = 4

        class HairLength(Enum):
            BALD = 0
            SHORT = 1
            MEDIUM = 2
            LONG = 3
            VERY_LONG = 4

    logger = None
    # rooms = None <-- need this?

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Utility() class", self.logger)

    async def send_message(self, event_object, websocket):
        method_name = inspect.currentframe().f_code.co_name
        msg = event_object.to_json()
        LogUtils.debug(f"{method_name}: enter, {msg}", self.logger)
        LogUtils.debug(f"{method_name}: Sending json: {msg}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        await websocket.send(str(msg))

    def generate_location(self, rooms):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        id = random.choice(rooms).id
        LogUtils.debug(f"{method_name}: enter", self.logger)
        return id

    def generate_name(self, include_identifier=True, include_sirname=False):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        name_choice = random.choice(self.common_names)
        identifier = ""
        sirname_choice = ""

        # sirname list
        if include_sirname:
            sirname_choice = random.choice(self.common_sirnames)
            
        # title list
        if include_identifier:
            identifier = random.choice(self.common_identifiers)

        # combine name and title
        name = f"{sirname_choice.strip()} {name_choice.strip()} {identifier.strip()}".strip()

        LogUtils.debug(f"{method_name}: exit, returing: {name}", self.logger)

        return name

    def create_unique_name(self, original_name):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        name = f"{original_name}_{int(time.time())}".lower()
        LogUtils.debug(f"{method_name}: exit, returning: {name}", self.logger)
        return name

    def sanitize_filename(self, filename):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        new_filename = "".join(i for i in filename if i.isalnum())
        LogUtils.debug(f"{method_name}: exit, returning: {new_filename}", self.logger)
        return new_filename
