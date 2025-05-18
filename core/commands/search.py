from random import random
from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility


class Search:
    logger = None
    command = "search"
    examples = ["search", "sea"]
    description = "Search area"
    type = CommandEnum.SEARCH

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Search() class")

    async def execute(self, player: PlayerData):
        self.logger.debug("enter")
        rand = random()
        success = rand < (player.attributes.perception / 100)
        if success is True:
            if len(self.world_service.rooms.rooms[player.room.id].hidden_items) > 0:
                for item in self.world_service.rooms.rooms[player.room.id].hidden_items:
                    await InfoEvent(f"You found {item.name}!").send(player.websocket)

                    # remove from "hidden items"
                    self.world_service.rooms.rooms[player.room.id].hidden_items.remove(item)

                    # add to items in room
                    self.world_service.rooms.rooms[player.room.id].items.append(item)
            else:
                await InfoEvent(
                        "After an exhaustive search, you find nothing and give up."
                    ).send(player.websocket)
        else:
            await InfoEvent(f"{player.selected_character.name} searches the room but finds nothing.").send(player.websocket)

        self.logger.info(f"player {player.selected_character.name} search yielded results: {success}")
        self.logger.debug("exit")
