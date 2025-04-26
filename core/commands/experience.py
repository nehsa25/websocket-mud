from core.enums.commands import CommandEnum
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
from utilities.events import EventUtility


class Experience:
    logger = None
    description = "Show experience"
    command = "experience[exp]"
    examples = ["exp", "experience"]
    type = CommandEnum.EXPERIENCE

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Experience() class")

    async def execute(self, player):
        self.logger.debug("enter")
        await EventUtility.send_message(
            InfoEvent(f"You have {player.experience} experience."), player.websocket
        )
        self.logger.debug("exit")
        return player
