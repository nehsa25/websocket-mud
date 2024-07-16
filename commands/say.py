import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Say(Utility):
    logger = None
    command = "say <message>"
    examples = []
    description = "Say something to the room you're in."
    type = Utility.Share.Commands.SAY
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Say() class", self.logger)

    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        player.room = await world_state.get_room(player.room)
        msg = command.split(" ", 1)[1]
        await self.send_message(MudEvents.CommandEvent(f'You say "{msg}"'), player.websocket)
        await player.room.alert(f"{player.name} says \"{msg}\"", exclude_player=True, player=player, event_type=MudEvents.InfoEvent)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player