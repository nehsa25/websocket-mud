from core.enums.commands import CommandEnum
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class Who:
    logger = None
    command = "who"
    examples = ["who"]
    description = "List all players in the game."
    type = CommandEnum.WHO

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Who() class")

    async def execute(self, player, world_state):
        self.logger.debug("enter")
        players = ""
        for player in world_state.players.players:
            players += f"{player.name}<br>"

        await EventUtility.send_message(
            EventUtility.AnnouncementEvent(f"Players Online:<br>{players}"),
            player.websocket,
        )
        self.logger.debug("exit")
        return player
