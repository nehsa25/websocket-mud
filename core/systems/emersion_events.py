import asyncio
from datetime import datetime
from random import randint, random
from core.enums.time_of_day import TimeOfDayEnum
from core.events.environment import EnvironmentEvent
from core.events.time import TimeEvent
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class EmersionEvents:
    logger = None
    shutdown = False
    
    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing EmersionEvents() class")

        self.logger.debug("Done initializing EmersionEvents() class")

    async def setup(self):
        await self.rain()
        await self.thunder()
        await self.breeze()
        await self.eerie_silence()
        await self.being_observed()
        await self.bang()
        await self.day_or_night()
        await self.get_system_time()

    # A startling bang..
    async def bang(self):
        self.logger.debug("enter")
        bang_type = ""
        while not self.shutdown:
            rand = randint(2000, 3800 * 3)
            self.logger.debug(
                f"A startling bang will occur in {str(rand)} seconds...",
                self.logger,
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
            msg = f"You hear a {bang_type} {distance}.."
            for p in self.players.players:
                await self.send_message(EnvironmentEvent(msg), p.websocket)

    # sets day or night
    async def day_or_night(self):
        self.logger.debug("enter")

        if self.dayornight == TimeOfDayEnum.NIGHT:
            await self.alert_world(
                "It is night.", event_type=EnvironmentEvent
            )
        else:
            await self.alert_world(
                "You see light off to the distance. It is daytime.", event_type=EnvironmentEvent
            )

        # for each monster in room still alive
        while not self.shutdown:
            await asyncio.sleep(self.dayornight_interval * 60)
            self.logger.info(
                f"{method_name}: Checking: check_day_or_night", self.logger
            )
            self.dayornight = (
                TimeOfDayEnum.DAY
                if self.dayornight == TimeOfDayEnum.NIGHT
                else TimeOfDayEnum.NIGHT
            )
            await self.alert_world(
                f"It is now {self.dayornight.name.lower()}.",
                event_type=EnvironmentEvent,
            )

    # just return the current date/time
    async def get_system_time(self):
        self.logger.debug("enter")
        while not self.shutdown:
            time = datetime.datetime.now().strftime("%I:%M%p on %B %d")
            for p in self.players.players:
                await self.send_message(TimeEvent(time), p.websocket)

            # sleep 10 minutes
            await asyncio.sleep(60 * 10)
            self.logger.info("Checking: get_system_time")

    # It begins to rain..
    async def rain(self):
        while not self.shutdown:
            rand = randint(2000, 3600 * 2)
            self.logger.debug(f"Will run rain1 event in {str(rand)} seconds...")
            await asyncio.sleep(rand)
            for p in self.players.players:
                await EventUtility.send_message(
                    EnvironmentEvent("It begins to rain.."),
                    p.websocket,
                )

            # wait for it to stop
            rand = randint(100, 500)
            self.logger.debug(f"Will run rain2 event in {str(rand)} seconds...")
            await asyncio.sleep(rand)
            for p in self.players.players:
                await EventUtility.send_message(
                    EnvironmentEvent(
                        "The rain pitter-patters to a stop and the sun begins to shine through the clouds.."
                    ),
                    p.websocket,
                )

    # You hear thunder off in the distane..
    async def thunder(self):
        while not self.shutdown:
            rand = randint(2000, 3800 * 2)
            self.logger.debug(f"Will run thunder event in {str(rand)} seconds...")
            await asyncio.sleep(rand)
            self.logger.info("Checking: thunder")
            for p in self.players.players:
                await EventUtility.send_message(
                    EnvironmentEvent("You hear thunder off in the distance.."),
                    p.websocket,
                )

    # A gentle breeze blows by you..
    async def breeze(self):
        self.logger.debug("enter")
        while not self.shutdown:
            rand = randint(2000, 3800 * 2)
            self.logger.debug(f"Will run breeze event in {str(rand)} seconds...")
            await asyncio.sleep(rand)
            self.logger.info("Checking: breeze")
            for p in self.players.players:
                await EventUtility.send_message(
                    EnvironmentEvent("A gentle breeze blows by you.."),
                    p.websocket,
                )

    # An eerie silence settles on the room..
    async def eerie_silence(self):
        self.logger.debug("enter")
        while not self.shutdown:
            rand = randint(2000, 4000 * 2)
            self.logger.debug(
                f"Will run eerie_silence event in {str(rand)} seconds...",
                self.logger,
            )
            await asyncio.sleep(rand)
            self.logger.info("Checking: eerie_silence")
            for p in self.players.players:
                await EventUtility.send_message(
                    EnvironmentEvent("An eerie silence engulfs the area.."),
                    p.websocket,
                )

    # Eyes are watching you..
    async def being_observed(self):
        self.logger.debug("enter")
        while not self.shutdown:
            rand = randint(2000, 9000 * 2)
            self.logger.debug(
                f"You are being watched event will run in {str(rand)} seconds...",
                self.logger,
            )
            await asyncio.sleep(rand)
            self.logger.info("Checking: being_observed")
            for p in self.players.players:
                await EventUtility.send_message(
                    EnvironmentEvent(
                        "You are being observed. You glance around and behind you but cannot determine from where."
                    ),
                    p.websocket,
                )
