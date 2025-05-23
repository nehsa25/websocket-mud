from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility


class Experience:
    logger = None
    description = "Show experience"
    command = "experience[exp]"
    examples = ["exp", "experience"]
    type = CommandEnum.EXPERIENCE

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Experience() class")

    async def execute(self, player: PlayerData):
        self.logger.debug("enter")
        await InfoEvent(f"You have {player.experience} experience.").send(player.websocket)
        self.logger.debug("exit")
