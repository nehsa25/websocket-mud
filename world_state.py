import asyncio
from copy import deepcopy
import datetime
import inspect
from random import randint
import random
import time
import traceback

import websockets
from aiimages import AIImages
from environment import Environments
from locks import NpcLock
from map import Map
from monster import Monster
from mudevent import MudEvents
from players import Players
from utility import Utility
from log_utils import LogUtils

class WorldState(Utility):
    # ensures we don't run the same event twice
    event_tracker = []

    def __init__(self, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing WorldState() class", self.logger)

        # Initialize Players and Environments here
        self.players = Players(self.logger)
        self.environments = Environments(self.logger)

        self.weather = WorldState.Weather(self.logger)
        self.weather.logger = self.logger
        self.weather.start_description = "The sun is shining brightly."
        self.weather.weather_type = Utility.WeatherTypes.SUN
        self.weather.current_season = Utility.WeatherSeasons.SUMMER
        self.weather.weather_strength = Utility.WeatherStrength.LIGHT

        self.monsters = []
        self.npcs = []
        self.rooms = []
        self.running_map_threads = [] 
        self.running_image_threads = [] 
        self.map = Map(self.logger)
        self.aiimages = AIImages(self.logger)

    async def setup_world_events(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # populate monsters
        if len(self.monsters) == 0:
            self.monsters = deepcopy(Utility.Monsters)
            LogUtils.info(f"{method_name}: Populating monsters...", self.logger)
            for monster in self.monsters:
                LogUtils.debug(f"{method_name}: Monster: {monster.name}", self.logger)
        else:
            LogUtils.warn(f"{method_name}: Monsters already populated.", self.logger)

        # populate npcs
        if len(self.npcs) == 0:
            self.npcs = deepcopy(Utility.Npcs)
            LogUtils.info(f"{method_name}: Populating npcs...", self.logger)
            for npc in self.npcs:
                LogUtils.debug(f"{method_name}: Npc: {npc.name}", self.logger)
        else:
            LogUtils.warn(f"{method_name}: Npcs already populated.", self.logger)

        # populate rooms
        if len(self.rooms) == 0:
            self.rooms = deepcopy(self.environments.rooms)
            LogUtils.info(f"{method_name}: Populating rooms...", self.logger)
            for room in self.rooms:
                LogUtils.debug(f"{method_name}: Room: {room.name}", self.logger)
        else:
            LogUtils.warn(f"{method_name}: Rooms already populated.", self.logger)

        # setup weather events
        self.weather.eyeswatching_event = self.being_observed()
        #self.weather.check_for_attack_event = self.check_monster_events()
        self.weather.breeze_event = self.breeze()
        self.weather.rain_event = self.rain()
        self.weather.eerie_event = self.eerie_silence()
        self.weather.thunder_event = self.thunder()
        self.weather.time_event = self.get_system_time()
        self.weather.bang_event = self.bang()
        self.weather.dayornight_event = self.day_or_night()
        self.weather.admin_stats_event = self.get_admin_status()
        self.weather.get_weather_season_event = self.get_weather_season()
        self.weather.get_weather_event = self.get_weather()
        self.weather.monster_respawn_event = self.check_monster_events()

        # setup day or night
        asyncio.create_task(self.day_or_night())

        # setup weather
        asyncio.create_task(self.change_weather())

        # setup season
        asyncio.create_task(self.change_season())

        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def change_weather(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while True:
            await asyncio.sleep(self.weather.change_weather_in_min * 60)
            LogUtils.info(f"{method_name}: Changing weather...", self.logger)
            self.weather.weather_type = random.choice(list(Utility.WeatherType))
            LogUtils.info(f"{method_name}: Weather changed to {self.weather.weather_type}", self.logger)

    async def change_season(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while True:
            await asyncio.sleep(self.weather.change_season_in_min * 60)
            LogUtils.info(f"{method_name}: Changing season...", self.logger)
            self.weather.current_season = random.choice(list(Utility.Seasons))
            LogUtils.info(f"{method_name}: Season changed to {self.weather.current_season}", self.logger)

    async def day_or_night(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while True:
            await asyncio.sleep(self.weather.dayornight_interval * 60)
            LogUtils.info(f"{method_name}: Changing day or night...", self.logger)
            if self.weather.dayornight == Utility.DayOrNight.DAY:
                self.weather.dayornight = Utility.DayOrNight.NIGHT
            else:
                self.weather.dayornight = Utility.DayOrNight.DAY
            LogUtils.info(f"{method_name}: Day or night changed to {self.weather.dayornight}", self.logger)

    class Weather:
        start_description = None
        weather_type = None
        current_season = None
        weather_strength = None
        change_weather_in_min = 120
        change_season_in_min = 120 * 8
        logger = None
        weather_room_description = None
        weather = None
        dayornight = Utility.DayOrNight.DAY
        dayornight_interval = 30
        eyeswatching_event = None
        check_for_attack_event = None
        breeze_event = None
        rain_event = None
        eerie_event = None
        thunder_event = None
        time_event = None
        bang_event = None
        dayornight_event = None
        admin_stats_event = None
        get_weather_season_event = None
        get_weather_event = None
        monster_respawn_event = None
        is_raining = False
        is_snowing = False
        is_storming = False

        def __init__(self, logger):
            self.weather_type = random.choice(list(Utility.WeatherTypes))
            self.weather_strength = random.choice(list(Utility.WeatherStrength))
            self.logger = logger
            LogUtils.debug("Initializing WorldEvents.Weather() class", self.logger)

            self.set_weather_descriptions()

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

            room_desc = room_description
            if self.is_raining:
                room_desc += " It is raining."
            elif self.is_snowing:
                room_desc += " It is snowing."
            elif self.is_storming:
                room_desc += " A storm rages."

            return room_desc

        def set_weather_descriptions(self):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            if (
                self.weather_type == Utility.WeatherTypes.RAIN
                and self.weather_strength == Utility.WeatherStrength.LIGHT
            ):
                self.weather_room_description = "There's currently a light drizzle."
                self.start_description = "It's starting to rain."
            elif (
                self.weather_type == Utility.WeatherTypes.RAIN
                and self.weather_strength == Utility.WeatherStrength.MEDIUM
            ):
                self.weather_room_description = "It's raining."
                self.start_description = "It's starting to rain hard."
            elif (
                self.weather_type == Utility.WeatherTypes.RAIN
                and self.weather_strength == Utility.WeatherStrength.HEAVY
            ):
                self.weather_room_description = "It's pouring rain."
                self.start_description = "It's starting to rain very hard."
            elif (
                self.weather_type == Utility.WeatherTypes.FOG
                and self.weather_strength == Utility.WeatherStrength.LIGHT
            ):
                self.weather_room_description = "A small fog has settled in."
                self.start_description = "A light fog begins to form."
            elif (
                self.weather_type == Utility.WeatherTypes.FOG
                and self.weather_strength == Utility.WeatherStrength.MEDIUM
            ):
                self.weather_room_description = "Fog has settled in."
                self.start_description = "A mild fog begins to form."
            elif (
                self.weather_type == Utility.WeatherTypes.FOG
                and self.weather_strength == Utility.WeatherStrength.HEAVY
            ):
                self.weather_room_description = "A thick fog has settled in. You can barely see your hand in front of your face."
                self.start_description = "A thick fog begins to form."
            elif (
                self.weather_type == Utility.WeatherTypes.SNOW
                and self.weather_strength == Utility.WeatherStrength.LIGHT
            ):
                self.weather_room_description = "Small flurry of snowflakes are falling."
                self.start_description = "It begins to snow."
            elif (
                self.weather_type == Utility.WeatherTypes.SNOW
                and self.weather_strength == Utility.WeatherStrength.MEDIUM
            ):
                self.weather_room_description = "It's snowing."
                self.start_description = "A decent snowfall abruptly begins."
            elif (
                self.weather_type == Utility.WeatherTypes.SNOW
                and self.weather_strength == Utility.WeatherStrength.HEAVY
            ):
                self.weather_room_description = (
                    "It's snowing heavily. You may want to find shelter."
                )
                self.start_description = "A heavy snowfall begins."
            elif (
                self.weather_type == Utility.WeatherTypes.THUNDER
                and self.weather_strength == Utility.WeatherStrength.LIGHT
            ):
                self.weather_room_description = "It's pouring rain."
                self.start_description = (
                    "It's starting to rain very hard. The sky is beginning to darken."
                )
            elif (
                self.weather_type == Utility.WeatherTypes.THUNDER
                and self.weather_strength == Utility.WeatherStrength.MEDIUM
            ):
                self.weather_room_description = "It's pouring rain and thundering."
                self.start_description = (
                    "A dilluge of rain begins. The sky is abuptly overcast."
                )
            elif (
                self.weather_type == Utility.WeatherTypes.THUNDER
                and self.weather_strength == Utility.WeatherStrength.HEAVY
            ):
                self.weather_room_description = "Lightning is striking all around you. The sound of thunder is all-consuming."
                self.start_description = "It's starting to rain very hard.  The sky is abuptly a dark gray overcast and lightning is beginning to strike."
            elif (
                self.weather_type == Utility.WeatherTypes.SUN
                and self.weather_strength == Utility.WeatherStrength.LIGHT
            ):
                self.weather_room_description = "The sun is shines down. It's pleasant."
                self.start_description = "Sun breaks through the clouds."
            elif (
                self.weather_type == Utility.WeatherTypes.SUN
                and self.weather_strength == Utility.WeatherStrength.MEDIUM
            ):
                self.weather_room_description = "The sun is shining brightly. You shade your eyes as you look around."
                self.start_description = "Sun breaks through the clouds."
            elif (
                self.weather_type == Utility.WeatherTypes.SUN
                and self.weather_strength == Utility.WeatherStrength.HEAVY
            ):
                self.weather_room_description = (
                    "A cloudless blue sky extends in all directions."
                )
                self.start_description = "Sun breaks through the clouds."
            elif (
                self.weather_type == Utility.WeatherTypes.OVERCAST
                and self.weather_strength == Utility.WeatherStrength.LIGHT
            ):
                self.weather_room_description = "Small patches of sun shine through the clouds."
                self.start_description = "Clouds are starting to form."
            elif (
                self.weather_type == Utility.WeatherTypes.OVERCAST
                and self.weather_strength == Utility.WeatherStrength.MEDIUM
            ):
                self.weather_room_description = "The sky is overcast."
                self.start_description = "Clouds are starting to form."
            elif (
                self.weather_type == Utility.WeatherTypes.OVERCAST
                and self.weather_strength == Utility.WeatherStrength.HEAVY
            ):
                self.weather_room_description = (
                    "The sky is completely overcast. It looks like it may rain soon."
                )
                self.start_description = "A heavy overcast begins to form."

    # returns the name of the area based on the type
    def get_area_identifier(self, area):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        result = ""
        for env in Utility.EnvironmentTypes:
            if area == env.name:
                result = env.name
        LogUtils.debug(f"{method_name}: exit, returning: {result}", self.logger)
        return result

    async def check_monster_events(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            monsters = []

            # run events
            for monster in self.environments.all_monsters:
                # wander
                if monster.wanders:
                    monsters.append(asyncio.create_task(self.mob_wander(monster, is_npc=False)))
                
                # check for dialog
                monsters.append(asyncio.create_task(self.npc_dialog(monster)))
                
                # check for combat
                monsters.append(asyncio.create_task(self.npc_check_for_combat(monster)))
                    
            await asyncio.gather(*monsters)

    async def check_npc_events(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            npcs = []

            # run events
            for npc in self.environments.all_npcs:
                # wander
                if npc.wanders:
                    npcs.append(asyncio.create_task(self.mob_wander(npc, is_npc=True)))
                
                # check for dialog
                npcs.append(asyncio.create_task(self.npc_dialog(npc)))
                
                # check for combat
                npcs.append(asyncio.create_task(self.npc_check_for_combat(npc)))
                    
            await asyncio.gather(*npcs)

    async def check_player_events(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            players = []

            # run events
            for player in self.players.players:
                
                # check for combat
                players.append(asyncio.create_task(self.player_check_for_combat(player)))
                    
            await asyncio.gather(*players)

    async def mob_wander(self, mob, is_npc=True):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)       
        npclock = NpcLock(mob)
        async with npclock.lock:
            rand = randint(0, 10)
            LogUtils.debug(
                f'NPC "{mob.name}" will move in {str(rand)} seconds...',
                self.logger,
            )
            await asyncio.sleep(rand)
            self = await mob.wander(self, is_npc)

        LogUtils.debug(f"{method_name}: exit", self.logger)
        
    async def npc_dialog(self, npc):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
     
        npclock = NpcLock(npc)
        async with npclock.lock:
            room = npc.room_id
            if len(room.players) == 0:
                return
            await npc.speak(room, self)
            rand = randint(60, 60 * 10)
            LogUtils.debug(
                f'NPC "{npc.name}" will speak again in {str(rand)} seconds if a player still in room...',
                self.logger,
            )
            await asyncio.sleep(rand)                

        LogUtils.debug(f"{method_name}: exit", self.logger)
        
    async def npc_check_for_combat(self, npc):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
         
        npclock = NpcLock(npc)
        async with npclock.lock:
            LogUtils.debug(f'NPC "{npc.name}" will checking combat',self.logger)  
            self = await npc.check_combat(self)

        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def player_check_for_combat(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
      
        npclock = NpcLock(player)
        async with npclock.lock:
            LogUtils.debug(f'Player "{player.name}" will checking combat',self.logger)  
            self = await player.check_combat()

        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def player_check_for_resting(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
           
        npclock = NpcLock(player)
        async with npclock.lock:
            LogUtils.debug(f'Player "{player.name}" will check if resting',self.logger)  
            self = await player.check_resting()

        LogUtils.debug(f"{method_name}: exit", self.logger)

    # A startling bang..
    async def bang(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        bang_type = ""
        while not self.shutdown:
            rand = randint(2000, 3800 * 3)
            LogUtils.debug(
                f"A startling bang will occur in {str(rand)} seconds...",
                self.logger,
            )
            await asyncio.sleep(rand)
            LogUtils.info(f"{method_name}: Checking: bang", self.logger)
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
            msg = f"You hear a {bang_type} {distance}.."
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent(msg), p.websocket
                )

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
            LogUtils.info(f"{method_name}: Checking: get_weather", self.logger)
            self.weather.weather_type = random.choice(
                list(Utility.WeatherTypes)
            )
            self.weather.start_description = self.weather.set_weather_descriptions()

    # Setup weather season event
    async def get_weather_season(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            asyncio.sleep(self.weather.change_weather_in_min * 60)
            LogUtils.info(
                f"{method_name}: Checking: get_weather_season", self.logger
            )

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
            LogUtils.info(f"{method_name}: Checking: rain", self.logger)
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent("It begins to rain.."),
                    p.websocket,
                )

            # wait for it to stop
            rand = randint(100, 500)
            LogUtils.debug(
                f"Will run rain2 event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent(
                        "The rain pitter-patters to a stop and the sun begins to shine through the clouds.."
                    ),
                    p.websocket,
                )

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
            LogUtils.info(f"{method_name}: Checking: thunder", self.logger)
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent(
                        "You hear thunder off in the distance.."
                    ),
                    p.websocket,
                )

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
            LogUtils.info(f"{method_name}: Checking: breeze", self.logger)
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent("A gentle breeze blows by you.."),
                    p.websocket,
                )

    # An eerie silence settles on the room..
    async def eerie_silence(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(2000, 4000 * 2)
            LogUtils.debug(
                f"Will run eerie_silence event in {str(rand)} seconds...",
                self.logger,
            )
            await asyncio.sleep(rand)
            LogUtils.info(f"{method_name}: Checking: eerie_silence", self.logger)
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent(
                        "An eerie silence engulfs the area.."
                    ),
                    p.websocket,
                )

    # Eyes are watching you..
    async def being_observed(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while not self.shutdown:
            rand = randint(2000, 9000 * 2)
            LogUtils.debug(
                f"You are being watched event will run in {str(rand)} seconds...",
                self.logger,
            )
            await asyncio.sleep(rand)
            LogUtils.info(f"{method_name}: Checking: being_observed", self.logger)
            for p in self.players.players:
                await self.send_message(
                    MudEvents.EnvironmentEvent(
                        "You are being observed. You glance around and behind you but cannot determine from where."
                    ),
                    p.websocket,
                )

    # admin status
    async def get_admin_status(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        while not self.shutdown:
            msg = "**************************************************<br>"
            msg += "World Statistics:<br>"
            msg += f"* Players: {len(self.players.players)}<br>"
            msg += "**************************************************"
            for p in self.players.players:
                await self.send_message(MudEvents.InfoEvent(msg), p.websocket)

            await asyncio.sleep(60 * 15)
            LogUtils.info(f"{method_name}: Checking: get_admin_status", self.logger)

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
            LogUtils.info(f"{method_name}: Checking: get_system_time", self.logger)

    # sets day or night
    async def check_day_or_night(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        if self.dayornight == Utility.DayOrNight.NIGHT:
            await self.alert_world(
                "It is night.", event_type=MudEvents.EnvironmentEvent
            )
        else:
            await self.alert_world(
                "It is daytime.", event_type=MudEvents.EnvironmentEvent
            )

        # for each monster in room still alive
        while not self.shutdown:
            await asyncio.sleep(self.dayornight_interval * 60)
            LogUtils.info(
                f"{method_name}: Checking: check_day_or_night", self.logger
            )
            self.dayornight = (
                Utility.DayOrNight.DAY
                if self.dayornight == Utility.DayOrNight.NIGHT
                else Utility.DayOrNight.NIGHT
            )
            await self.alert_world(
                f"It is now {self.dayornight.name.lower()}.",
                event_type=MudEvents.EnvironmentEvent,
            )

    async def populate_monsters(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        rooms = deepcopy(self.environments.rooms)
        monsters = []
        
        # add in monsters
        for room in rooms:
            room.monsters = []
            if random.randint(0, 1) <= room.monster_saturation:
                for i in range(room.scariness):
                    monster = None
                    m_type = random.choice(
                        list(Utility.Monsters)
                    )
                    monster = self.monster.get_monster(m_type, room)
                    if room.in_town and monster.allowed_in_city == False:
                        LogUtils.debug(
                            f'{method_name}: Will not add "{monster.name}" to room "{room.name}: not allowed in city"',
                            self.logger,
                        )
                        continue
                    LogUtils.debug(
                        f'{method_name}: Adding monster "{monster.name}" to room "{room.name}"',
                        self.logger,
                    )
                    room.monsters.append(monster)
                    monsters.append(monster)

            LogUtils.info(
                f"monsters added to {room.name}: {len(room.monsters)}", self.logger
            )

        LogUtils.debug(
            f"{method_name}: exit, monsters added: {len(room.monsters)}", self.logger
        )

        return monsters, rooms

    async def populate_npcs(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        npcs = []
        new_rooms = []
        rooms = deepcopy(self.environments.rooms)

        # add in npcs
        LogUtils.info(f"{method_name}: Adding NPCs..", self.logger)
        for room in rooms:            
            LogUtils.info(f"{method_name}: room: {room.name}", self.logger)
            new_room = deepcopy(room)
            for npc_type in new_room.npc_types:
                new_npc = self.environments.npcs.get_npc(npc_type, room)
                LogUtils.info(f"{method_name}: Adding npc \"{new_npc.name}\" to room \"{new_room.name}\"", self.logger)
                new_room.npcs.append(new_npc)
                npcs.append(new_npc)
                
            LogUtils.info(
                f"Added to room \"{new_room.name}\": {len(new_room.npcs)}", self.logger
            )
            new_rooms.append(new_room)

        LogUtils.debug(
            f"{method_name}: exit, npcs added: {len(room.npcs)}", self.logger
        )

        return npcs, new_rooms

    # returns player, world, responsible for moving a player from one room to the next
    async def move_room_player(self, new_room_id, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # add player to new room
        new_room = new_room_id
        new_room.players.append(player)

        # if the player has a previous room, update it
        if player.room is not None:
            old_room = player.room

            if old_room != new_room:
                for monster in old_room.monsters:
                    if monster.in_combat == player:
                        monster.in_combat = None

                # remove player from old room
                old_room.players.remove(player)

        # update to new room
        player.previous_room = player.room
        player.room = new_room

        # name for images
        map_image_name = self.sanitize_filename(
            self.create_unique_name(f"{player.name}_map")
        )  # renkath_map_1718628698
        room_image_name = (
            self.sanitize_filename(self.create_unique_name(f"{new_room.name}_room"))
            + ".png"
        )  # townsquare_room_1718628698

        # generate new map (in a new task so we don't block the player)
        self.running_map_threads.append(
            asyncio.create_task(
                self.map.generate_map(
                    new_room,
                    map_image_name,
                    player,
                    self,
                    self.get_area_identifier(new_room.environment),
                )
            )
        )

        # generate a new room image (in a new task so we don't block the player)
        self.running_image_threads.append(
            asyncio.create_task(
                self.aiimages.generate_image(
                    item_name=room_image_name,
                    item_description=new_room.description,
                    inside=new_room.inside,
                    player=player,
                    world_state=self,
                )
            )
        )

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, self

    # returns player, world, responsible for moving a monster from one room to the next
    async def move_room_monster(self, new_room_id, monster, direction):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # if the npc has a previous room, update it
        if monster.room_id is not None:
            await monster.room_id.alert(f"{monster.get_full_name()} has left to the {direction['direction'].name.capitalize()}!")
            if monster in monster.room_id.npcs:
                monster.room_id.npcs.remove(monster)

        # add player to new room
        new_room = new_room_id
        # print(await monster.announce_entrance(new_room))
        await new_room.alert(f"{monster.get_full_name()} approaches from the {direction["direction"].opposite.name.capitalize()}!")
        new_room.monsters.append(monster)

        # update to new room
        monster.prev_room_id = monster.room_id
        monster.room_id = new_room_id

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return monster, self

    # returns player, world, responsible for moving a npc from one room to the next
    async def move_room_npc(self, new_room_id, npc, direction):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # if the npc has a previous room, update it
        if npc.room_id is not None:
            await npc.room_id.alert(f"{npc.get_full_name()} has left to the {direction['direction'].name.capitalize()}.")
            if npc in npc.room_id.npcs:
                npc.room_id.npcs.remove(npc)

        # add player to new room
        new_room = new_room_id
        await new_room.alert(f"{npc.get_full_name()} approaches from the {direction["direction"].opposite.name.capitalize()}.")
        new_room.npcs.append(npc)

        # update to new room
        npc.prev_room_id = npc.room_id
        npc.room_id = new_room_id

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return npc, self

    # just returns a specific room in our list of rooms
    async def get_room(self, room_id):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, room_id: {room_id}", self.logger)
        room = [room for room in self.environments.rooms if room.name == room_id.name]
        LogUtils.debug(
            f'{method_name}: room "{room}"', self.logger
        )
        if room == []:
            raise Exception(f"Room {room_id} not found.")
        room = room[0]
        LogUtils.debug(
            f'{method_name}: exit, returning room "{room.name}"', self.logger
        )
        return room

    async def show_room(self, player, look_location_room=None):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        room = await self.get_room(player.room)
        if look_location_room is not None:
            room = await self.get_room(look_location_room)
            
        # get the description
        if room.inside:
            description = room.description
        else:
            description = self.weather.add_weather_description(room.description)
        room.description = description
        # room_def = room.BasicRoom(room)
        
        # show items
        items = ""
        if len(room.items) > 0:
            for item in room.items:
                items += item.name + ", "
            items = items[0 : len(items) - 2]

        # offer possible exits
        exits = ""
        for available_exit in room.exits:
            exits += available_exit["direction"].name + ", "
        exits = exits[0 : len(exits) - 2]

        # show npcs
        npcs = ""
        for npc in room.npcs:
            new_npc = npc.name
            if npc.title is not None and npc.title != "":
                new_npc = f"{npc.title} {npc.name}"
            npcs += new_npc + ", "
        npcs = npcs[0 : len(npcs) - 2]
        LogUtils.info(f"npcs in room: {npcs}", self.logger)

        # show monsters
        monsters = ""
        for monster in room.monsters:
            monsters += monster.name + ", "
        monsters = monsters[0 : len(monsters) - 2]
        LogUtils.info(f"Monsters in room: {monsters}", self.logger)

        # show people
        people = ""
        for p in room.players:
            if player.name == p.name:
                continue
            if p.room.name == player.room.name:
                people += p.name + ", "
        if people != "":
            people = people[0 : len(people) - 2]

        # formulate message to client
        # room_event = MudEvents.RoomEvent(
        #     room_def.name, room_def.description, room_def.items, room_def.exits, room_def.monsters, room_def.players, room_def.npcs
        # )
        
        room_event = MudEvents.RoomEvent(
            room.name, description, items, exits, monsters, people, npcs
        )
        await self.send_message(room_event, player.websocket)

        return room
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def update_item_in_room(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        for place, item in enumerate(self.environments.rooms.items):
            print(place, item)
                # self.environments.rooms[place] = item
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def remove_room(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.active_rooms.remove(room)

    async def update_room(self, room, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        for r in world.environments.rooms:
            if r.name == room.name:
                r = room
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return world.environments

    async def alert_world(
        self, message, exclude_player=True, player=None, event_type=MudEvents.InfoEvent
    ):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, message: {message}", self.logger)
        for p in self.players.players:
            if exclude_player and player is not None:
                if p.name != player.name:
                    await self.send_message(event_type(message), p.websocket)
            else:
                await self.send_message(MudEvents.InfoEvent(message), p.websocket)

        LogUtils.debug(f"{method_name}: exit", self.logger)
