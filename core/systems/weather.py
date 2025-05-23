
import asyncio
from random import random
from core.enums.time_of_day import TimeOfDayEnum
from core.enums.weather_seasons import WeatherSeasonEnum
from core.enums.weather_strength_levels import WeatherStrengthEnum
from core.enums.weather_types import WeatherTypeEnum
from utilities.log_telemetry import LogTelemetryUtility


class Weather:
    start_description = "The sun is shining brightly."
    weather_type = None
    current_season = None
    weather_strength = None
    change_weather_in_min = 120
    change_season_in_min = 120 * 8
    logger = None
    weather_room_description = None
    weather = None
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
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Weather class")    

        self.weather_type = random.choice(list(WeatherTypeEnum))
        self.weather_strength = random.choice(list(WeatherStrengthEnum))       
        self.weather_type = WeatherTypeEnum.SUN
        self.current_season = WeatherSeasonEnum.SUMMER
        self.weather_strength = WeatherStrengthEnum.LIGHT
        self.set_weather_descriptions() 

        # setup weather events
        self.admin_stats_event = self.get_admin_status()
        self.get_weather_season_event = self.get_weather_season()
        self.get_weather_event = self.get_weather()
        self.monster_respawn_event = self.check_monster_events()

        # setup day or night
        asyncio.create_task(self.day_or_night())

        # setup weather
        asyncio.create_task(self.change_weather())

        # setup season
        asyncio.create_task(self.change_season())
        
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
        if self.weather_type == WeatherTypeEnum.RAIN and self.weather_strength == WeatherStrengthEnum.LIGHT:
            self.weather_room_description = "There's currently a light drizzle."
            self.start_description = "It's starting to rain."
        elif self.weather_type == WeatherTypeEnum.RAIN and self.weather_strength == WeatherStrengthEnum.MEDIUM:
            self.weather_room_description = "It's raining."
            self.start_description = "It's starting to rain hard."
        elif self.weather_type == WeatherTypeEnum.RAIN and self.weather_strength == WeatherStrengthEnum.HEAVY:
            self.weather_room_description = "It's pouring rain."
            self.start_description = "It's starting to rain very hard."
        elif self.weather_type == WeatherTypeEnum.FOG and self.weather_strength == WeatherStrengthEnum.LIGHT:
            self.weather_room_description = "A small fog has settled in."
            self.start_description = "A light fog begins to form."
        elif self.weather_type == WeatherTypeEnum.FOG and self.weather_strength == WeatherStrengthEnum.MEDIUM:
            self.weather_room_description = "Fog has settled in."
            self.start_description = "A mild fog begins to form."
        elif self.weather_type == WeatherTypeEnum.FOG and self.weather_strength == WeatherStrengthEnum.HEAVY:
            self.weather_room_description = (
                "A thick fog has settled in. You can barely see your hand in front of your face."
            )
            self.start_description = "A thick fog begins to form."
        elif self.weather_type == WeatherTypeEnum.SNOW and self.weather_strength == WeatherStrengthEnum.LIGHT:
            self.weather_room_description = "Small flurry of snowflakes are falling."
            self.start_description = "It begins to snow."
        elif self.weather_type == WeatherTypeEnum.SNOW and self.weather_strength == WeatherStrengthEnum.MEDIUM:
            self.weather_room_description = "It's snowing."
            self.start_description = "A decent snowfall abruptly begins."
        elif self.weather_type == WeatherTypeEnum.SNOW and self.weather_strength == WeatherStrengthEnum.HEAVY:
            self.weather_room_description = "It's snowing heavily. You may want to find shelter."
            self.start_description = "A heavy snowfall begins."
        elif self.weather_type == WeatherTypeEnum.THUNDER and self.weather_strength == WeatherStrengthEnum.LIGHT:
            self.weather_room_description = "It's pouring rain."
            self.start_description = "It's starting to rain very hard. The sky is beginning to darken."
        elif self.weather_type == WeatherTypeEnum.THUNDER and self.weather_strength == WeatherStrengthEnum.MEDIUM:
            self.weather_room_description = "It's pouring rain and thundering."
            self.start_description = "A dilluge of rain begins. The sky is abuptly overcast."
        elif self.weather_type == WeatherTypeEnum.THUNDER and self.weather_strength == WeatherStrengthEnum.HEAVY:
            self.weather_room_description = (
                "Lightning is striking all around you. The sound of thunder is all-consuming."
            )
            self.start_description = (
                "It's starting to rain very hard.  "
                "The sky is abuptly a dark gray overcast and "
                "lightning is beginning to strike."
            )
        elif self.weather_type == WeatherTypeEnum.SUN and self.weather_strength == WeatherStrengthEnum.LIGHT:
            self.weather_room_description = "The sun is shines down. It's pleasant."
            self.start_description = "Sun breaks through the clouds."
        elif self.weather_type == WeatherTypeEnum.SUN and self.weather_strength == WeatherStrengthEnum.MEDIUM:
            self.weather_room_description = "The sun is shining brightly. You shade your eyes as you look around."
            self.start_description = "Sun breaks through the clouds."
        elif self.weather_type == WeatherTypeEnum.SUN and self.weather_strength == WeatherStrengthEnum.HEAVY:
            self.weather_room_description = "A cloudless blue sky extends in all directions."
            self.start_description = "Sun breaks through the clouds."
        elif self.weather_type == WeatherTypeEnum.OVERCAST and self.weather_strength == WeatherStrengthEnum.LIGHT:
            self.weather_room_description = "Small patches of sun shine through the clouds."
            self.start_description = "Clouds are starting to form."
        elif self.weather_type == WeatherTypeEnum.OVERCAST and self.weather_strength == WeatherStrengthEnum.MEDIUM:
            self.weather_room_description = "The sky is overcast."
            self.start_description = "Clouds are starting to form."
        elif self.weather_type == WeatherTypeEnum.OVERCAST and self.weather_strength == WeatherStrengthEnum.HEAVY:
            self.weather_room_description = "The sky is completely overcast. It looks like it may rain soon."
            self.start_description = "A heavy overcast begins to form."

    async def day_or_night(self):
        self.logger.debug("enter")
        while True:
            await asyncio.sleep(self.dayornight_interval * 60)
            self.logger.info("Changing day or night...")
            if self.dayornight == TimeOfDayEnum.NOON:
                self.dayornight = TimeOfDayEnum.NIGHT
            else:
                self.dayornight = TimeOfDayEnum.NOON
            self.logger.info(f"Day or night changed to {self.dayornight}")

    async def change_weather_random(self):
        self.logger.debug("enter")
        while True:
            await asyncio.sleep(self.weather.change_weather_in_min * 60)
            self.logger.info("Changing weather...")
            self.weather_type = random.choice(list(WeatherTypeEnum))
            self.weather_strength = random.choice(list(WeatherStrengthEnum))
            self.logger.info(f"Weather changed to {self.weather.weather_type}")

    async def change_season(self):
        self.logger.debug("enter")
        while True:
            await asyncio.sleep(self.weather.change_season_in_min * 60)
            self.logger.info("Changing season...")
            self.current_season = random.choice(list(WeatherSeasonEnum))
            self.logger.info(f"Season changed to {self.weather.current_season}")
