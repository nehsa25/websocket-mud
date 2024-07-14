import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Experience(Utility):
    logger = None
    description = "Display how much experience you have and how much is needed to progress to next level."
    command = "experience[exp]"
    examples = []
    type = Utility.Share.Commands.EXPERIENCE
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Experience() class", self.logger)
        
    async def execute(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await self.send_message(MudEvents.InfoEvent(f"You have {player.experience} experience."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
