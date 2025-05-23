
import asyncio
from core.enums.send_scope import SendScopeEnum
from core.enums.time_of_day import TimeOfDayEnum
from core.events.info import InfoEvent
from services.world import WorldService
from utilities.log_telemetry import LogTelemetryUtility


class TimeOfDay:
    dayornight = None
    dayornight_interval = 120  # in minutes

    def __init__(self, world_service: WorldService):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing TimeOfDay() class")   
        self.world_service = world_service  

    async def start(self):
        self.logger.debug("Starting TimeOfDay() class")

        # setup day or night
        asyncio.create_task(self.time_loop())

    async def time_loop(self):
        self.logger.debug("enter")
        while True:
            await asyncio.sleep(self.dayornight_interval * 60)
            
            if self.dayornight == TimeOfDayEnum.NOON:
                self.dayornight = TimeOfDayEnum.NIGHT
            else:
                self.dayornight = TimeOfDayEnum.NOON
            
            self.logger.info(f"Updating time of day to: {self.dayornight}")

            await self.send_time()

    async def send_time(self):
        self.logger.debug("enter")
        msg = "It is now " + self.dayornight.name.lower() + "."
        for player in self.world_service.player_registry.get_players():
                await InfoEvent(msg).send(player=player.websocket, scope=SendScopeEnum.PLAYER)
        await InfoEvent(msg).send(scope=SendScopeEnum.WORLD)
