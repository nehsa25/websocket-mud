from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from utilities.log_telemetry import LogTelemetryUtility


class Get:
    logger = None
    description = "Get something"
    command = "get <target>"
    examples = [
        "g sword - get a sword",
    ]
    type = CommandEnum.GET

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Get() class")

    async def execute(self, command: str, player: PlayerData):
        self.logger.debug("enter")
        wanted_item = command.split(" ", 1)[1].lower()
        await player.inventory.get_item(wanted_item, player)
        self.logger.debug("exit")
