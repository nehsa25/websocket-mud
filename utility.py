from enum import Enum
import inspect
import random
from log_utils import LogUtils
from mudevent import MudEvents


class Utility(MudEvents):  
    class Share:
        WORLD_NAME = "Illisurom"
        PLAYER_BASE_REST_WAIT_SECS = 2
        
        class EnvironmentTypes(Enum):
            TOWNSMEE = 1,
            BEACH = 2,
            FOREST = 3,
            JUNGLE = 4,
            BREACH = 5,
            GRAVEYARD = 6
                    
        class DayOrNight(Enum):
            DAY = 1
            NIGHT = 2
                
        class Coin(Enum):
            Copper = 1
            Silver = 2
            Gold = 3
    
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

    def sanitize_filename(self, filename):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        new_filename = "".join(i for i in filename if i.isalnum())
        LogUtils.debug(f"{method_name}: exit, returning: {new_filename}", self.logger)
        return new_filename