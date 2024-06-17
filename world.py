import asyncio
import datetime
import inspect
from random import randint
import random
from mudevent import MudEvents
from players import Players
from map import Map
from monsters import Monsters
from rooms import Rooms
from utility import Utility
from log_utils import LogUtils
from command import Command

from utility import Utility


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

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing World() class", self.logger)

        if self.command is None:
            self.command = Command(self.logger)

        if self.rooms is None:
            self.rooms = Rooms(self.world_name, self.logger)

        if self.map is None:
            self.map = Map(self.rooms, self.logger)

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
            for world_player in self.players:
                await self.send_msg(
                    f"A {bang_type} can be heard off in the distance..",
                    "event",
                    world_player.websocket,
                )

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
            for world_player in self.players:
                await self.send_msg(
                    "It begins to rain..", "event", world_player.websocket
                )

            # wait for it to stop
            rand = randint(100, 500)
            LogUtils.debug(
                f"Will run rain2 event in {str(rand)} seconds...", self.logger
            )
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.send_msg(
                    "The rain pitter-patters to a stop and the sun begins to shine through the clouds..",
                    "event",
                    world_player.websocket,
                )

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
            for world_player in self.players:
                await self.send_msg(
                    "You hear thunder off in the distance..",
                    "event",
                    world_player.websocket,
                )

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
            for world_player in self.players:
                await self.send_msg(
                    "A gentle breeze blows by you..", "event", world_player.websocket
                )

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
            for world_player in self.players:
                await self.send_msg(
                    "An eerie silence settles on the room..",
                    "event",
                    world_player.websocket,
                )

    # just return the current date/time
    async def get_system_time(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        while True:
            time = datetime.datetime.now().strftime("%I:%M%p on %B %d")
            for world_player in self.players.players:
                time_event = MudEvents.TimeEvent(time).to_json()
                await self.send_message(time_event, world_player.websocket)

            # sleep 10 minutes
            await asyncio.sleep(60 * 10)
