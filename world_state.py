import asyncio
from copy import deepcopy
import random
from random import randint
from game.ai.image import AIImages
from game.enums.monsters import Monsters
from game.enums.npcs import Npcs
from game.enums.time_of_day import TimeOfDay
from game.enums.weather_seasons import WeatherSeasons
from game.enums.weather_strength_levels import WeatherStrength
from game.enums.weather_types import WeatherTypes
from game.environment import Environments
from game.locks import NpcLock
from game.map import Map
from utilities.log_telemetry import LogTelemetryUtility


class WorldState:
    # ensures we don't run the same event twice
    event_tracker = []

    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing WorldState() class")

        # Initialize Players and Environments here
        self.environments = Environments()
        self.weather = WorldState.Weather()
        self.weather.logger = self.logger
        self.weather.start_description = "The sun is shining brightly."
        self.weather.weather_type = WeatherTypes.SUN
        self.weather.current_season = WeatherSeasons.SUMMER
        self.weather.weather_strength = WeatherStrength.LIGHT

        self.monsters = []
        self.npcs = []
        self.rooms = []
        self.running_map_threads = []
        self.running_image_threads = []
        self.map = Map()
        self.aiimages = AIImages()

    async def setup_world_events(self):
        self.logger.debug("enter")

        # populate monsters
        if len(self.monsters) == 0:
            self.monsters = deepcopy(Monsters)
            self.logger.info("Populating monsters...")
            for monster in self.monsters:
                self.logger.debug(f"Monster: {monster.name}")
        else:
            LogTelemetryUtility.warn("Monsters already populated.")

        # populate npcs
        if len(self.npcs) == 0:
            self.npcs = deepcopy(Npcs)
            self.logger.info("Populating npcs...")
            for npc in self.npcs:
                self.logger.debug(f"Npc: {npc.name}")
        else:
            LogTelemetryUtility.warn("Npcs already populated.")

        # populate rooms
        if len(self.rooms) == 0:
            self.rooms = deepcopy(self.environments.rooms)
            self.logger.info("Populating rooms...")
            for room in self.rooms:
                self.logger.debug(f"Room: {room.name}")
        else:
            LogTelemetryUtility.warn("Rooms already populated.")

        # setup weather events
        self.weather.eyeswatching_event = self.being_observed()
        # self.weather.check_for_attack_event = self.check_monster_events()
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

        self.logger.debug("exit")

    async def change_weather(self):
        self.logger.debug("enter")
        while True:
            await asyncio.sleep(self.weather.change_weather_in_min * 60)
            self.logger.info("Changing weather...")
            self.weather.weather_type = random.choice(list(WeatherTypes))
            self.logger.info(f"Weather changed to {self.weather.weather_type}")

    async def change_season(self):
        self.logger.debug("enter")
        while True:
            await asyncio.sleep(self.weather.change_season_in_min * 60)
            self.logger.info("Changing season...")
            self.weather.current_season = random.choice(list(WeatherSeasons))
            self.logger.info(f"Season changed to {self.weather.current_season}")

    async def day_or_night(self):
        self.logger.debug("enter")
        while True:
            await asyncio.sleep(self.weather.dayornight_interval * 60)
            self.logger.info("Changing day or night...")
            if self.weather.dayornight == TimeOfDay.NOON:
                self.weather.dayornight = TimeOfDay.NIGHT
            else:
                self.weather.dayornight = TimeOfDay.NOON
            self.logger.info(f"Day or night changed to {self.weather.dayornight}")

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
        dayornight = TimeOfDay.NOON
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

        def __init__(self):
            self.weather_type = random.choice(list(WeatherTypes))
            self.weather_strength = random.choice(list(WeatherStrength))
            self.logger = LogTelemetryUtility.get_logger(__name__)
            self.logger.debug("Initializing WorldEvents.Weather() class")

            self.set_weather_descriptions()

        async def change_weather(self, weather_type, weather_strength):
            self.logger.debug("enter")
            self.weather_type = weather_type
            self.weather_strength = weather_strength
            self.set_weather_descriptions()
            self.logger.debug("exit")

        def add_weather_description(self, room_description):
            self.logger.debug("enter")

            room_desc = room_description
            if self.is_raining:
                room_desc += " It is raining."
            elif self.is_snowing:
                room_desc += " It is snowing."
            elif self.is_storming:
                room_desc += " A storm rages."

            return room_desc

        def set_weather_descriptions(self):
            self.logger.debug("enter")
            if self.weather_type == WeatherTypes.RAIN and self.weather_strength == WeatherStrength.LIGHT:
                self.weather_room_description = "There's currently a light drizzle."
                self.start_description = "It's starting to rain."
            elif self.weather_type == WeatherTypes.RAIN and self.weather_strength == WeatherStrength.MEDIUM:
                self.weather_room_description = "It's raining."
                self.start_description = "It's starting to rain hard."
            elif self.weather_type == WeatherTypes.RAIN and self.weather_strength == WeatherStrength.HEAVY:
                self.weather_room_description = "It's pouring rain."
                self.start_description = "It's starting to rain very hard."
            elif self.weather_type == WeatherTypes.FOG and self.weather_strength == WeatherStrength.LIGHT:
                self.weather_room_description = "A small fog has settled in."
                self.start_description = "A light fog begins to form."
            elif self.weather_type == WeatherTypes.FOG and self.weather_strength == WeatherStrength.MEDIUM:
                self.weather_room_description = "Fog has settled in."
                self.start_description = "A mild fog begins to form."
            elif self.weather_type == WeatherTypes.FOG and self.weather_strength == WeatherStrength.HEAVY:
                self.weather_room_description = (
                    "A thick fog has settled in. You can barely see your hand in front of your face."
                )
                self.start_description = "A thick fog begins to form."
            elif self.weather_type == WeatherTypes.SNOW and self.weather_strength == WeatherStrength.LIGHT:
                self.weather_room_description = "Small flurry of snowflakes are falling."
                self.start_description = "It begins to snow."
            elif self.weather_type == WeatherTypes.SNOW and self.weather_strength == WeatherStrength.MEDIUM:
                self.weather_room_description = "It's snowing."
                self.start_description = "A decent snowfall abruptly begins."
            elif self.weather_type == WeatherTypes.SNOW and self.weather_strength == WeatherStrength.HEAVY:
                self.weather_room_description = "It's snowing heavily. You may want to find shelter."
                self.start_description = "A heavy snowfall begins."
            elif self.weather_type == WeatherTypes.THUNDER and self.weather_strength == WeatherStrength.LIGHT:
                self.weather_room_description = "It's pouring rain."
                self.start_description = "It's starting to rain very hard. The sky is beginning to darken."
            elif self.weather_type == WeatherTypes.THUNDER and self.weather_strength == WeatherStrength.MEDIUM:
                self.weather_room_description = "It's pouring rain and thundering."
                self.start_description = "A dilluge of rain begins. The sky is abuptly overcast."
            elif self.weather_type == WeatherTypes.THUNDER and self.weather_strength == WeatherStrength.HEAVY:
                self.weather_room_description = (
                    "Lightning is striking all around you. The sound of thunder is all-consuming."
                )
                self.start_description = (
                    "It's starting to rain very hard.  "
                    "The sky is abuptly a dark gray overcast and "
                    "lightning is beginning to strike."
                )
            elif self.weather_type == WeatherTypes.SUN and self.weather_strength == WeatherStrength.LIGHT:
                self.weather_room_description = "The sun is shines down. It's pleasant."
                self.start_description = "Sun breaks through the clouds."
            elif self.weather_type == WeatherTypes.SUN and self.weather_strength == WeatherStrength.MEDIUM:
                self.weather_room_description = "The sun is shining brightly. You shade your eyes as you look around."
                self.start_description = "Sun breaks through the clouds."
            elif self.weather_type == WeatherTypes.SUN and self.weather_strength == WeatherStrength.HEAVY:
                self.weather_room_description = "A cloudless blue sky extends in all directions."
                self.start_description = "Sun breaks through the clouds."
            elif self.weather_type == WeatherTypes.OVERCAST and self.weather_strength == WeatherStrength.LIGHT:
                self.weather_room_description = "Small patches of sun shine through the clouds."
                self.start_description = "Clouds are starting to form."
            elif self.weather_type == WeatherTypes.OVERCAST and self.weather_strength == WeatherStrength.MEDIUM:
                self.weather_room_description = "The sky is overcast."
                self.start_description = "Clouds are starting to form."
            elif self.weather_type == WeatherTypes.OVERCAST and self.weather_strength == WeatherStrength.HEAVY:
                self.weather_room_description = "The sky is completely overcast. It looks like it may rain soon."
                self.start_description = "A heavy overcast begins to form."

    # returns the name of the area based on the type
    def get_area_identifier(self, area):
        self.logger.debug("enter")
        result = ""
        for env in Environments:
            if area == env.name:
                result = env.name
        self.logger.debug(f"exit, returning: {result}")
        return result

    async def check_monster_events(self):
        self.logger.debug("enter")
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
        self.logger.debug("enter")
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
        self.logger.debug("enter")
        # while not self.shutdown:
        #     players = []

        #     # run events
        #     for player in self.players.players:
        #         # check for combat
        #         players.append(asyncio.create_task(self.player_check_for_combat(player)))

        #     await asyncio.gather(*players)

    async def mob_wander(self, mob, is_npc=True):
        self.logger.debug("enter")
        npclock = NpcLock(mob)
        async with npclock.lock:
            rand = randint(0, 10)
            self.logger.debug(f'NPC "{mob.name}" will move in {str(rand)} seconds...')
            await asyncio.sleep(rand)
            self = await mob.wander
