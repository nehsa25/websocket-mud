import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Telepath(Utility):
    logger = None
    command = "telepath[tele] <target> <message>"
    examples = []
    description = "Communicate to another another player who is not in the same room via your mind!"
    type = Utility.Share.Commands.TELEPATHY
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Telepath() class", self.logger)

    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        target_player_name = command.split(" ", 1)[1].split(" ", 1)[0]
        msg = command.split(" ", 1)[1]        
        target_player = world_state.players.find_player_by_name(target_player_name)
        if target_player is not None and player.can_telepath():
            await self.send_message(MudEvents.CommandEvent(f'You whisper "{msg}" to {target_player.name}'), player.websocket)
            await target_player.websocket.send(MudEvents.CommandEvent(f'{player.name} whispers "{msg}" to you.'))        
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player