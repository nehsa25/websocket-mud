import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Who(Utility):
    logger = None
    command = "who"
    examples = ["who"]
    description = "List all players in the game."
    type = Utility.Share.Commands.WHO
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Who() class", self.logger)

    async def execute(self, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        players = ""
        for player in world_state.players.players:
            players += f"{player.name}<br>"

        await self.send_message(MudEvents.AnnouncementEvent(f"Players Online:<br>{players}"), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
