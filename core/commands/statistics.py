from core.enums.commands import CommandEnum
from core.events.info import InfoEvent
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class Statistics:
    logger = None
    command = "statistics"
    examples = ["stats", "statistics"]
    description = "View character statistics"
    type = CommandEnum.STATISTICS

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Statistics() class")

    async def execute(self, player):
        self.logger.debug("enter")
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
        await EventUtility.send_message(InfoEvent(player_stats), player.websocket)
        self.logger.debug("exit")
        return player
