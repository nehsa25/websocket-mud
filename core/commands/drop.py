from core.data.player_data import PlayerData
from utilities.log_telemetry import LogTelemetryUtility
from core.enums.commands import CommandEnum


class Drop:
    logger = None
    description = "Drop an item to the ground"
    command = "drop <target>"
    examples = [
        "d sword - drop a sword",
    ]
    type = CommandEnum.DROP

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Drop() class")

    async def execute(self, command: str, player: PlayerData):
        self.logger.debug("enter")
        wanted_item = command.split(" ", 1)[1].lower()
        await player.inventory.drop_item(wanted_item, player)
        self.logger.debug("exit")
