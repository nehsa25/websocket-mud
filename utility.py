from enum import Enum
import inspect
import random
import time
from log_utils import LogUtils
from mudevent import MudEvents

class Utility(MudEvents):  
    class Share:
        WORLD_NAME = "Illisurom"
        PLAYER_BASE_REST_WAIT_SECS = 2
        EVENT_SPEED = PLAYER_BASE_REST_WAIT_SECS
        
        class EnvironmentTypes(Enum):
            TOWNSMEE = 1,
            BEACH = 2,
            FOREST = 3,
            JUNGLE = 4,
            BREACH = 5,
            GRAVEYARD = 6
            
        class Races(Enum):
            HUMAN = 0,
            KOBOLD = 1,
            GOBLIN = 2,
            HALFLING = 3,
            HALFOGRE = 4,
            ORC = 5,
            ELF = 6,
            FAE = 7,
            NYRRISS = 8,
            ARGUNA = 9,
            EAREA = 10
            
        class Classes(Enum):
            WARRIOR = 0,
            MAGE = 1,
            THIEF = 2,
            CLERIC = 3,
            RANGER = 4,
            DRUID = 5,
            BARD = 6,
            PALADIN = 7,
            MONK = 8,
            BARBARIAN = 9,
            WARLOCK = 10,
            SORCERER = 11,
            ROGUE = 12,
            BERSERKER = 13,
            BATTLE_MAGE = 14,
            BOWMAN = 15,
            KNIGHT = 16,
            NECROMANCER = 17,
            ILLUSIONIST = 18
            
        class MudDirections:  # directions
            up = ["u", "up"]
            down = ["d", "down"]
            north = ["n", "north", "nor"]
            south = ["s", "south", "sou"]
            east = ["e", "east", "eas", "ea"]
            west = ["w", "west", "wes", "we"]
            northwest = ["nw", "northwest", "northw"]
            northeast = ["ne", "northeast", "northe"]
            southeast = ["se", "southeast", "southe"]
            southwest = ["sw", "southwest", "southw"]
            directions = [
                up[0].lower(),
                up[1].lower(),
                down[0].lower(),
                down[1].lower(),
                north[0].lower(),
                north[1].lower(),
                north[2].lower(),
                south[0].lower(),
                south[1].lower(),
                south[2].lower(),
                east[0].lower(),
                east[1].lower(),
                east[2].lower(),
                west[0].lower(),
                west[1].lower(),
                west[2].lower(),
                northwest[0].lower(),
                northwest[1].lower(),
                northwest[2].lower(),
                northeast[0].lower(),
                northeast[1].lower(),
                northeast[2].lower(),
                southeast[0].lower(),
                southeast[1].lower(),
                southeast[2].lower(),
                southwest[0].lower(),
                southwest[1].lower(),
                southwest[2].lower(),
            ]
            pretty_directions = [
                up,
                down,
                north,
                south,
                east,
                west,
                northwest,
                northeast,
                southeast,
                southwest,
            ]

            opp_directions = [
                (up, down),
                (east, west),
                (north, south),
                (northeast, southwest),
                (northwest, southeast),
            ]
                   
            @staticmethod
            def get_friendly_name( direction):
                friendly_name = None
                for pretty_direction in Utility.Share.MudDirections.pretty_directions:
                    if direction in pretty_direction:
                        friendly_name = pretty_direction[1].capitalize()
                        break
                return friendly_name
            
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
    
        class Alignment(Enum):
            GOOD = 1  # attacks evil players only
            NEUTRAL = 2  # only attacks if attacked
            EVIL = 3  # attacks good players only
            CHOATIC = 4  # attacks all players
    
        class EnvironmentTypes(Enum):
            TOWNSMEE = 1,
            BEACH = 2,
            FOREST = 3,
            JUNGLE = 4,
            BREACH = 5,
            GRAVEYARD = 6
        
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

    def is_valid_look_direction(self, direction):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        found = False
        for valid_direction in Utility.Share.MudDirections.pretty_directions:
            if direction.lower() in valid_direction:
                found = True
                break
            
        LogUtils.info(f"Is valid look direction? {found}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return found
        
    def generate_name(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        names = []
        names.append("Ley")
        names.append("Sirius")
        names.append("Capella")
        names.append("Regulus")
        names.append("Stride")
        names.append("Betelgeuse")
        names.append("Holo")
        name_choice = random.randint(0, len(names) - 1)

        # title list
        titles = []
        titles.append("the Brave")
        titles.append("the Cowardly")
        titles.append("the Fool")
        titles.append("the greedy")
        titles.append("the Prideful")
        titles.append("the Wise")
        title_choice = random.randint(0, len(titles) - 1)

        # combine name and title
        name = f"{names[name_choice]} {titles[title_choice]}"
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