from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.events.command import CommandEvent
from utilities.log_telemetry import LogTelemetryUtility


class Telepath:
    logger = None
    command = "telepath[tele] <target> <message>"
    examples = []
    description = "Communicate to another another player who is not in the same room via your mind!"
    type = CommandEnum.TELEPATHY

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Telepath() class")

    async def execute(self, command: str, player: PlayerData):
        self.logger.debug("enter")
        target_player_name = command.split(" ", 1)[1].split(" ", 1)[0]
        msg = command.split(" ", 1)[1]
        target_player = self.players.find_player_by_name(target_player_name)
        if target_player is not None and player.can_telepath():
            await CommandEvent(f'You whisper "{msg}" to {target_player.selected_character.name}').send(player.websocket)
            await CommandEvent(f'{player.selected_character.name} whispers "{msg}" to you.').send(target_player.websocket)

        self.logger.debug("exit")