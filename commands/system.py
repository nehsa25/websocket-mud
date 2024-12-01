import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class System(Utility):
    logger = None
    command = "system <subcommand> <args>"
    examples = [
        "system name Hopper - change your name to Hopper",
        "sys name Kvothe",
        "sys name - open change name modal"
    ]
    description = "Perform a system command"
    type = Utility.Share.Commands.SYSTEM
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing System() class", self.logger)

    async def execute(self, command, extra, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_command = command.split(" ")
        action_to_take = None
        request = None
        if len(wanted_command) < 1:
            await self.send_message(MudEvents.ErrorEvent("Invalid system command"), player.websocket)
            return player
        
        # this is the acton component of the command
        action_to_take = wanted_command[1]

        if action_to_take == "name":
            if len(wanted_command) == 3 or extra:

                request = wanted_command[2].capitalize()

            player.name = request

            # check if user already in system (they should be)
            world_state = await world_state.players.unregister(player, world_state, change_name=True)
            player, world_state = await world_state.players.register(player, world_state)
            await self.send_message(MudEvents.UsernameChangedEvent(f"You are now known as {player.name}", player.name), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
