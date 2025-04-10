import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Statistics(Utility):
    logger = None
    command = "statistics"
    examples = [
        "stats",
        "statistics"
    ]
    description = "View character statistics"
    type = Utility.Commands.STATISTICS
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Statistics() class", self.logger)

    async def execute(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        player_stats = f"""        
        Hello {player.name}<br>
        **************************************************<br>
        Level: {player.level}<br>
        Experience: {player.experience}<br>
        **************************************************<br>
        Race: {player.race.name}<br>
        Class: {player.player_class.name}<br>
        **************************************************<br>
        You have the following attributes:<br>
        * Health {player.current_hp} of {player.max_hp}<br>
        * Strength {player.attributes.strength}<br>
        * Agility {player.attributes.agility}<br>
        * Determination {player.attributes.determination}<br>
        * Faith {player.attributes.faith}<br>
        * Intelligence {player.attributes.intelligence}<br>
        * Perception {player.attributes.perception}<br>
        Current Conditions and Aielments:<br>
        * Mood {player.statuses.mood.name.capitalize()}<br>
        * Resting {player.statuses.is_resting}<br>
        * Poisoned {player.statuses.is_poisoned}<br>
        **************************************************<br>
        """
        await self.send_message(MudEvents.InfoEvent(player_stats), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
