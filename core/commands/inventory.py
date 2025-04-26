from utilities.log_telemetry import LogTelemetryUtility
from core.enums.commands import CommandEnum


class Inventory:
    logger = None
    command = "inventory"
    examples = [
        "i",
        "inv",
        "inventory",
    ]
    description = "View inventory"
    type = CommandEnum.INVENTORY

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Inventory() class")
        self.items = []  # Initialize the items list here

    async def execute(self, player):
        self.logger.debug("enter")
        await player.send_inventory()
        self.logger.debug("exit")
