from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.events.info import InfoEvent
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

    async def execute(self, player: PlayerData):
        self.logger.debug("enter")
        player_stats = f"""        
        Hello {player.selected_character.name}<br>
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
        * dexterity {player.attributes.dexterity}<br>
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
        await InfoEvent(player_stats).send(player.websocket)
        self.logger.debug("exit")