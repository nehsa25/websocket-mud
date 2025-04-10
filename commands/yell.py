import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Yell(Utility):
    logger = None
    command = "yell <message>"
    examples = []
    description = "Speak loud enough for everyone to heard in adcacent rooms."
    type = Utility.Commands.YELL
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Yell() class", self.logger)

    async def execute(self, command, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        msg = command.split(" ", 1)[1]
        adjacent_message = "You hear a loud yell from the adjacent room."
        await self.send_message(MudEvents.CommandEvent(f'You yell "{msg}"'), player.websocket)
        await player.room.alert(f"{player.name} yells \"{msg}\"", exclude_player=True, player=player, event_type=MudEvents.InfoEvent, adjacent=adjacent_message)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player