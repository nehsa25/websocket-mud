from core.enums.commands import CommandEnum
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility


class Yell:
    logger = None
    command = "yell <message>"
    examples = []
    description = "Speak loud enough for everyone to heard in adcacent rooms."
    type = CommandEnum.YELL

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Yell() class")

    async def execute(self, command, player):
        self.logger.debug("enter")
        msg = command.split(" ", 1)[1]
        adjacent_message = "You hear a loud yell from the adjacent room."
        await InfoEvent(f'You yell "{msg}"').send(player.websocket)
        await InfoEvent(
            f'{player.name} yells "{msg}"',
            exclude_player=True,
            adjacent=adjacent_message,
        ).send(player.websocket)
        self.logger.debug("exit")
        return player
