import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Rest(Utility):
    logger = None
    command = "rest"
    examples = []
    description = "Rest and regain your health."
    type = Utility.Share.Commands.REST
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Rest() class", self.logger)

    async def execute(self, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        monsters_in_room = len(player.room.monsters)
        if player.in_combat == True or monsters_in_room > 0:
            player.stats.is_resting = False
            await self.send_message(MudEvents.RestEvent("You cannot rest at this time.  You are in combat.", rest_error=True, is_resting=False), player.websocket)
        else:
            # message staying you're starting to rest
            await self.send_message(MudEvents.RestEvent("You settle to rest.", rest_error=False, is_resting=True), player.websocket)

            # set an attribute that we can use later
            player.stats.is_resting = True

        # press enter (refresh the room)
        await world_state.show_room(player)

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return  player, world_state
