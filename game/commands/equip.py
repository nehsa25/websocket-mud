from game.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
from game.enums.commands import Commands
from utilities.events import EventUtility


class Equip:
    logger = None
    description = "Equip something"
    command = "eq <target>"
    examples = ["eq sword", "wield sword", "equip sword"]
    type = Commands.EQUIP

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Equip() class")

    async def execute(self, command, player):
        self.logger.debug("enter")
        wanted_item = command.split(" ", 1)[1]
        found_item = None

        # check if the item is in our inventory
        for item in player.inventory.items:
            if item.name.lower() == wanted_item.lower():
                await EventUtility.send_message(
                    InfoEvent(f"You equip {item.name}."), player.websocket
                )
                item.equipped = True
                found_item = True
                found_item = item

        # if you eq'd an item, deselect any previous items
        for item in player.inventory.items:
            if (
                found_item.item_type == item.item_type and item.equipped is True
            ) and found_item.name != item.name:
                await EventUtility.send_message(
                    f"You unequip {item.name}.", "info", player.websocket
                )
                item.equipped = False
        if found_item is None:
            await EventUtility.send_message(
                f"You cannot equip {wanted_item}.", "error", player.websocket
            )
        self.logger.debug("exit")
        return player
