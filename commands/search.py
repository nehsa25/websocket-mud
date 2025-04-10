import inspect
from random import random
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Search(Utility):
    logger = None
    command = "search"
    examples = [
        "search",
        "sea"
    ]
    description = "Search area"
    type = Utility.Commands.SEARCH
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Search() class", self.logger)

    async def execute(self, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        rand = random()
        success = rand < (player.stats.perception / 100)
        if success == True:
            if len(world_state.rooms.rooms[player.room.id].hidden_items) > 0:
                for item in world_state.rooms.rooms[player.room.id].hidden_items:
                    await self.send_message(MudEvents.InfoEvent(f"You found {item.name}!"), player.websocket)

                    # remove from "hidden items"
                    world_state.rooms.rooms[player.room.id].hidden_items.remove(item)

                    # add to items in room
                    world_state.rooms.rooms[player.room.id].items.append(item)
            else:
                await self.send_message(MudEvents.InfoEvent("After an exhaustive search, you find nothing and give up."), player.websocket)
        else:
            await self.send_message(MudEvents.InfoEvent("You search around but notice nothing."), player.websocket)

        LogUtils.info(f"{method_name}: player {player.name} search yielded results: {success}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
