from utilities.log_telemetry import LogTelemetryUtility
from game.enums.commands import Commands


class Drop:
    logger = None
    description = "Drop an item to the ground"
    command = "drop <target>"
    examples = [
        "d sword - drop a sword",
    ]
    type = Commands.DROP

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Drop() class")

    async def execute(self, command, player, world_state):
        self.logger.debug("enter")
        wanted_item = command.split(" ", 1)[1].lower()
        await player.inventory.drop_item(wanted_item, player)
        self.logger.debug("exit")
        return player, world_state
