import asyncio
import datetime
from enum import Enum
import inspect
from random import randint
import random
from aiimages import AIImages
from battles import Battles
from mudevent import MudEvents
from players import Players
from map import Map
from monsters import Monsters
from rooms import Rooms
from utility import Utility
from log_utils import LogUtils
from command import Command

class World(Utility):
    
    class Weather:

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
           
        start_description = None
        weather_type = None
        current_season = None   
        weather_strength = None     
        change_weather_in_min = 120
        change_season_in_min = 120 * 8
        logger = None
        room_description = None
        
        def __init__(self, weather_type, weather_strength, logger):
            self.weather_type = weather_type
            self.weather_strength = weather_strength
            self.logger = logger
            LogUtils.debug("Initializing Weather() class", self.logger)
            
        async def change_weather(self, weather_type, weather_strength):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            self.weather_type = weather_type
            self.weather_strength = weather_strength
            self.set_weather_descriptions()
            LogUtils.debug(f"{method_name}: exit", self.logger)
            
        def add_weather_description(self, room_description):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            room_desc = f"{room_description} {self.room_description}"
            LogUtils.debug(f"{method_name}: exit", self.logger)
            return room_desc
        
        def set_weather_descriptions(self):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            if self.weather_type == World.Weather.WeatherTypes.RAIN and self.weather_strength == World.Weather.WeatherStrength.LIGHT:
                self.room_description = "There's currently a light drizzle."
                self.start_description = "It's starting to rain."
            elif self.weather_type == World.Weather.WeatherTypes.RAIN and self.weather_strength == World.Weather.WeatherStrength.MEDIUM:
                self.room_description = "It's raining."
                self.start_description = "It's starting to rain hard."
            elif self.weather_type == World.Weather.WeatherTypes.RAIN and self.weather_strength == World.Weather.WeatherStrength.HEAVY:
                self.room_description = "It's pouring rain."
                self.start_description = "It's starting to rain very hard."
            elif self.weather_type == World.Weather.WeatherTypes.FOG and self.weather_strength == World.Weather.WeatherStrength.LIGHT:
                self.room_description = "A small fog has settled in."
                self.start_description = "A light fog begins to form."
            elif self.weather_type == World.Weather.WeatherTypes.FOG and self.weather_strength == World.Weather.WeatherStrength.MEDIUM:
                self.room_description = "Fog has settled in."
                self.start_description = "A mild fog begins to form."
            elif self.weather_type == World.Weather.WeatherTypes.FOG and self.weather_strength == World.Weather.WeatherStrength.HEAVY:
                self.room_description = "A thick fog has settled in. You can barely see your hand in front of your face."
                self.start_description = "A thick fog begins to form."
            elif self.weather_type == World.Weather.WeatherTypes.SNOW and self.weather_strength == World.Weather.WeatherStrength.LIGHT:
                self.room_description = "Small flurry of snowflakes are falling."
                self.start_description = "It begins to snow."
            elif self.weather_type == World.Weather.WeatherTypes.SNOW and self.weather_strength == World.Weather.WeatherStrength.MEDIUM:
                self.room_description = "It's snowing."
                self.start_description = "A decent snowfall abruptly begins."
            elif self.weather_type == World.Weather.WeatherTypes.SNOW and self.weather_strength == World.Weather.WeatherStrength.HEAVY:
                self.room_description = "It's snowing heavily. You may want to find shelter."
                self.start_description = "A heavy snowfall begins."
            elif self.weather_type == World.Weather.WeatherTypes.THUNDER and self.weather_strength == World.Weather.WeatherStrength.LIGHT:
                self.room_description = "It's pouring rain."
                self.start_description = "It's starting to rain very hard. The sky is beginning to darken."
            elif self.weather_type == World.Weather.WeatherTypes.THUNDER and self.weather_strength == World.Weather.WeatherStrength.MEDIUM:
                self.room_description = "It's pouring rain and thundering."
                self.start_description = "A dilluge of rain begins. The sky is abuptly overcast."
            elif self.weather_type == World.Weather.WeatherTypes.THUNDER and self.weather_strength == World.Weather.WeatherStrength.HEAVY:
                self.room_description = "Lightning is striking all around you. The sound of thunder is all-consuming."
                self.start_description = "It's starting to rain very hard.  The sky is abuptly a dark gray overcast and lightning is beginning to strike."
            elif self.weather_type == World.Weather.WeatherTypes.SUN and self.weather_strength == World.Weather.WeatherStrength.LIGHT:
                self.room_description = "The sun is shines down. It's pleasant."
                self.start_description = "Sun breaks through the clouds."
            elif self.weather_type == World.Weather.WeatherTypes.SUN and self.weather_strength == World.Weather.WeatherStrength.MEDIUM:
                self.room_description = "The sun is shining brightly. You shade your eyes as you look around."
                self.start_description = "Sun breaks through the clouds."
            elif self.weather_type == World.Weather.WeatherTypes.SUN and self.weather_strength == World.Weather.WeatherStrength.HEAVY:
                self.room_description = "A cloudless blue sky extends in all directions."
                self.start_description = "Sun breaks through the clouds."
            elif self.weather_type == World.Weather.WeatherTypes.OVERCAST and self.weather_strength == World.Weather.WeatherStrength.LIGHT:
                self.room_description = "Small patches of sun shine through the clouds."
                self.start_description = "Clouds are starting to form."
            elif self.weather_type == World.Weather.WeatherTypes.OVERCAST and self.weather_strength == World.Weather.WeatherStrength.MEDIUM:
                self.room_description = "The sky is overcast."
                self.start_description = "Clouds are starting to form."
            elif self.weather_type == World.Weather.WeatherTypes.OVERCAST and self.weather_strength == World.Weather.WeatherStrength.HEAVY:
                self.room_description = "The sky is completely overcast. It looks like it may rain soon."   
                self.start_description = "A heavy overcast begins to form."         
            
    class DayOrNight(Enum):
        DAY = 1
        NIGHT = 2
        
    world_name = "Illisurom"
    map = None
    logger = None
    utility = None
    command = None
    rooms = None
    players = None
    monsters = None
    ai_images = None
    shutdown = False
    dayornight = DayOrNight.DAY
    dayornight_interval = 30
    weather = None
    
    # monsters / fighting
    combats_in_progress = []

    # events
    eyeswatching_event = None
    check_for_attack_event = None
    breeze_event = None
    rain_event = None
    eerie_event = None
    thunder_event = None
    time_event = None
    bang_event = None
    battles = None
    dayornight_event = None
    admin_stats_event = None
    get_weather_season_event = None
    get_weather_event = None

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing World() class", self.logger)

        if self.weather is None:
            self.weather = World.Weather(World.Weather.WeatherTypes.FOG, World.Weather.WeatherStrength.MEDIUM, self.logger)
            self.weather.set_weather_descriptions()
            
        if self.command is None:
            self.command = Command(self.logger)

        if self.rooms is None:
            self.rooms = Rooms(self.world_name, self.logger)

        if self.map is None:
            self.map = Map(self.logger)
            
        if self.ai_images is None:
            self.ai_images = AIImages(self.logger)
            
        if self.players is None:
            self.players = Players(self.logger)

        if self.monsters is None:
            self.monsters = Monsters(self.logger)

        if self.battles is None:
            self.battles = Battles(self.logger)

    # schedule some events that'll do shit
    async def setup_world_events(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if self.breeze_event is None:
            self.breeze_event = asyncio.create_task(self.breeze())

        if self.rain_event is None:
            self.rain_event = asyncio.create_task(self.rain())

        if self.eerie_event is None:
            self.eerie_event = asyncio.create_task(self.eerie_silence())

        if self.thunder_event is None:
            self.thunder_event = asyncio.create_task(self.thunder())

        if self.time_event is None:
            self.time_event = asyncio.create_task(self.get_system_time())

        if self.eyeswatching_event is None:
            self.eyeswatching_event = asyncio.create_task(self.being_observed())

        if self.bang_event is None:
            self.time_event = asyncio.create_task(self.bang())

        if self.check_for_attack_event is None:
            self.check_for_attack_event = asyncio.create_task(
                self.check_for_combat()
            )

        if self.dayornight_event is None:
            self.dayornight_event = asyncio.create_task(
                self.check_day_or_night()
            )
            
        if self.admin_stats_event is None:
            self.admin_stats_event = asyncio.create_task(
                self.get_admin_status()
            )
            
        if self.get_weather_event is None:
            self.get_weather_event = asyncio.create_task(
                self.get_weather()
            )
            
        if self.get_weather_season_event is None:
            self.get_weather_season_event = asyncio.create_task(
                self.get_weather()
            )


        # start our resurrection task
        asyncio.create_task(self.monsters.respawn_mobs(self.rooms.rooms))

    # A startling bang..
    async def bang(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        bang_type = ""
        while not self.shutdown:
            rand = randint(2000, 3800 * 3)
            LogUtils.debug(
                f"A startling bang will occur in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            bang_type = random.choice(
                [
                    "sharp bang",
                    "dull thump",
                    "startling bang",
                    "loud crash",
                    "thunderous boom",
                ]
            )
            distance = random.choice(
                [
                    "off in the distance.",
                    "behind you.",
                    "to your left.",
                ]
            )
            msg = f"You hear a {bang_type} {distance}...."
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent(msg), p.websocket)

    # Setup weather event
    async def get_weather(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(500, self.weather.change_weather_in_min * 60)
            LogUtils.debug(
                f"Will run weather event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            
            self.weather.weather_type = random.choice(list(self.Weather.WeatherTypes))
            self.weather.start_description = self.weather.set_weather_descriptions()
            
    # Setup weather season event
    async def get_weather_season(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:            
            asyncio.sleep(self.weather.change_weather_in_min * 60)

    # It begins to rain..
    async def rain(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(2000, 3600 * 2)
            LogUtils.debug(
                f"Will run rain1 event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent("It begins to rain.."), p.websocket)

            # wait for it to stop
            rand = randint(100, 500)
            LogUtils.debug(
                f"Will run rain2 event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent("The rain pitter-patters to a stop and the sun begins to shine through the clouds.."), p.websocket)

    # You hear thunder off in the distane..
    async def thunder(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(2000, 3800 * 2)
            LogUtils.debug(
                f"Will run thunder event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent("You hear thunder off in the distance.."), p.websocket)

    # A gentle breeze blows by you..
    async def breeze(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(2000, 3800 * 2)
            LogUtils.debug(
                f"Will run breeze event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent("A gentle breeze blows by you."), p.websocket)

    # An eerie silence settles on the room..
    async def eerie_silence(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(2000, 4000 * 2)
            LogUtils.debug(
                f"Will run eerie_silence event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)            
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent("An eerie silence engulfs the area."), p.websocket)
                
    # Eyes are watching you..
    async def being_observed(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(2000, 9000 * 2)
            LogUtils.debug(
                f"You are being watched event will run in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)            
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent("You are being observed. You glance around and behind you but cannot determine from where."), p.websocket)
       
    # admin status
    async def get_admin_status(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)        

        while not self.shutdown:
            msg = "**************************************************<br>"
            msg += "World Statistics:<br>"
            msg += f"* Monsters in combat: {self.monsters_fighting}<br>"
            msg += "**************************************************"      
            for p in self.players.players:
                await self.send_message(MudEvents.InfoEvent(msg), p.websocket)
                
            await asyncio.sleep(60)  
            
    # just return the current date/time
    async def get_system_time(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            time = datetime.datetime.now().strftime("%I:%M%p on %B %d")
            for p in self.players.players:
                await self.send_message(MudEvents.TimeEvent(time), p.websocket)

            # sleep 10 minutes
            await asyncio.sleep(60 * 10)

    # responsible for the "prepares to attack you messages"
    async def check_for_combat(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        battle = None
        while not self.shutdown:
            await asyncio.sleep(2)
            battle, room, self = await self.battles.run_combat_round(battle, self.players, world=self)
            if battle.state == battle.BattleState.COMPLETED:
                self.battles = await battle.stop_battle(room, battle, self)

        LogUtils.debug(f"{method_name}: exit", self.logger)

    # sets day or night
    async def check_day_or_night(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        if self.dayornight == World.DayOrNight.NIGHT:
            await self.alert_world("It is night.", self, event_type=MudEvents.EnvironmentEvent)
        else:
            await self.alert_world("It is daytime.", self, event_type=MudEvents.EnvironmentEvent)
        
        # for each monster in room still alive
        while not self.shutdown:
            await asyncio.sleep(self.dayornight_interval * 60)
            self.dayornight = World.DayOrNight.DAY if self.dayornight == World.DayOrNight.NIGHT else World.DayOrNight.NIGHT
            await self.alert_world(f"It is now {self.dayornight.name.lower()}.", self, event_type=MudEvents.EnvironmentEvent)
