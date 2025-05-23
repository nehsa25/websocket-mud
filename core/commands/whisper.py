from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.events.command import CommandEvent
from utilities.log_telemetry import LogTelemetryUtility


class Whisper:
    logger = None
    command = "whisper <target> <message>"
    examples = []
    description = "Communicate to another another player in the same room privately."
    type = CommandEnum.WHISPER

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Whisper() class")

    async def execute(self, command: str, player: PlayerData):
        self.logger.debug("enter")
        target_player_name = command.split(" ", 1)[1].split(" ", 1)[0]
        player.room = await self.world_service.get_room(player.room)
        msg = command.split(" ", 1)[1]
        target_player = self.world_service.player_registry.players.find_player_by_name(target_player_name)
        if target_player is not None and target_player.room == player.room:
            await CommandEvent(f'You whisper "{msg}" to {target_player.selected_character.name}').send(player.websocket)
            await CommandEvent(f'{player.selected_character.name} whispers "{msg}" to you.').send(target_player.websocket)
            
        self.logger.debug("exit")
