from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
from core.enums.commands import CommandEnum


class Equip:
    logger = None
    description = "Equip something"
    command = "eq <target>"
    examples = ["eq sword", "wield sword", "equip sword"]
    type = CommandEnum.EQUIP

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
                await InfoEvent(
                    f"{player.name} equips {item.name}.", player.room.id
                ).send(player.websocket)
                item.equipped = True
                found_item = True
                found_item = item

        # if you eq'd an item, deselect any previous items
        for item in player.inventory.items:
            if (
                found_item.item_type == item.item_type and item.equipped is True
            ) and found_item.name != item.name:
                await InfoEvent(
                    f"{player.name} unequips {item.name}.", player.room.id
                ).send(player.websocket)
                item.equipped = False
        if found_item is None:
            await InfoEvent(
                f"{player.name} tried to equip {wanted_item}.", player.room.id
            ).send(player.websocket)
        self.logger.debug("exit")
        return player
