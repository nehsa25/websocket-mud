import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class System(Utility):
    logger = None
    command = "system[sys] <subcommand> <args>"
    examples = ["system name Hopper - change your name to Hopper"]
    description = "Perform a system command"
    type = Utility.Share.Commands.SYSTEM
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing System() class", self.logger)

    async def execute(self, command, extra, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_command = command.split(" ")
        subcmd = None
        request = None
        if len(wanted_command) == 3:
            subcmd = wanted_command[1]
            request = wanted_command[2].capitalize()

        if subcmd == "name":
            player.name = request

            # check if user already in system (they should be)
            world_state = await world_state.players.unregister(player, world_state, change_name=True)
            player, world_state = await world_state.players.register(player, world_state)
            await self.send_message(MudEvents.InfoEvent(f"You are now known as {player.name}"), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
