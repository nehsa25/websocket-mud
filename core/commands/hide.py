from core.data.player_data import PlayerData
from core.events.error import ErrorEvent
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
from core.enums.commands import CommandEnum


class Hide:
    logger = None
    command = "hide[hid,h], hide[hid,h] <item>, stash[st,s] <item>"
    examples = [
        "hide - hide yourself",
        "hide sword - hide an item",
        "stash coin - same as hide",
    ]
    description = "Hide yourself or an item in the room."
    type = CommandEnum.HIDE

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Hide() class")

    async def execute(self, command: str, player: PlayerData):
        self.logger.debug("enter")
        wanted_item = command.split(" ", 1)[1]
        found_item = False

        # check if it's in our inventory
        item_obj = None
        for item_in_inv in player.items.inventory:
            if wanted_item.lower() == item_in_inv.name.lower():
                item_obj = item_in_inv
                found_item = True
                break

        if found_item is True:
            # remove from inventory
            player.inventory.items.remove(item_obj)
            await InfoEvent(
                f"{player.selected_character.name} hid {item_obj.name}.", player.room.id
            ).send(player.websocket)
            self.world_service.rooms.rooms[player.room.id].hidden_items.append(item_obj)
        else:
            await ErrorEvent(f"You aren't carrying {wanted_item} to hide.").send(player.websocket)
        self.logger.debug("exit")