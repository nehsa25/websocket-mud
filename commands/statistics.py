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
        * Health {player.stats.current_hp} of {player.stats.max_hp}<br>
        * Strength {player.stats.strength}<br>
        * Agility {player.stats.agility}<br>
        * Determination {player.stats.determination}<br>
        * Faith {player.stats.faith}<br>
        * Intelligence {player.stats.intelligence}<br>
        * Perception {player.stats.perception}<br>
        Current Conditions and Aielments:<br>
        * Feriocity {player.stats.feriocity.name.capitalize()}<br>
        * Resting {player.stats.is_resting}<br>
        * Poisoned {player.stats.is_posioned}<br>
        **************************************************<br>
        """
        await self.send_message(MudEvents.InfoEvent(player_stats), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
