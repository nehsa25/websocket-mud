import asyncio
import datetime
import inspect
from random import randint
import random
from aiimages import AIImages
from mudevent import MudEvents
from players import Players
from map import Map
from monsters import Monsters
from rooms import Rooms
from utility import Utility
from log_utils import LogUtils
from command import Command

class World(Utility):
    world_name = "Illisurom"
    map = None
    players = []
    breeze_task = None
    rain_task = None
    eerie_task = None
    thunder_task = None
    time_task = None
    logger = None
    utility = None
    command = None
    rooms = None
    players = None
    monsters = None
    bang_task = None
    ai_images = None
    eyeswatching = None

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing World() class", self.logger)

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

    # schedule some events that'll do shit
    async def setup_world_events(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if self.breeze_task is None:
            self.breeze_task = asyncio.create_task(self.breeze())

        if self.rain_task is None:
            self.rain_task = asyncio.create_task(self.rain())

        if self.eerie_task is None:
            self.eerie_task = asyncio.create_task(self.eerie_silence())

        if self.thunder_task is None:
            self.thunder_task = asyncio.create_task(self.thunder())

        if self.time_task is None:
            self.time_task = asyncio.create_task(self.get_system_time())

        if self.eyeswatching is None:
            self.eyeswatching = asyncio.create_task(self.being_observed())

        if self.bang_task is None:
            self.time_task = asyncio.create_task(self.bang())

        if self.monsters.mob_attack_task is None:
            self.monsters.mob_attack_task = asyncio.create_task(
                self.monsters.mob_combat()
            )

        # start our resurrection task
        asyncio.create_task(self.monsters.respawn_mobs(self.rooms.rooms))

    # A startling bang..
    async def bang(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        bang_type = ""
        while True:
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
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent(bang_type), p.websocket)

    # It begins to rain..
    async def rain(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while True:
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
        while True:
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
        while True:
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
        while True:
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
        while True:
            rand = randint(2000, 9000 * 2)
            LogUtils.debug(
                f"You are being watched event will run in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)            
            for p in self.players.players:
                await self.send_message(MudEvents.EnvironmentEvent("You are being observed. You glance around and behind you but cannot determine from where."), p.websocket)
                
    # just return the current date/time
    async def get_system_time(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while True:
            time = datetime.datetime.now().strftime("%I:%M%p on %B %d")
            for p in self.players.players:
                await self.send_message(MudEvents.TimeEvent(time), p.websocket)

            # sleep 10 minutes
            await asyncio.sleep(60 * 10)
