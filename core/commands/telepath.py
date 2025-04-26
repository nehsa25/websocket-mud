from core.enums.commands import CommandEnum
from core.events.command import CommandEvent
from utilities.events import EventUtility
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

    async def execute(self, command, player, world_state):
        self.logger.debug("enter")
        target_player_name = command.split(" ", 1)[1].split(" ", 1)[0]
        msg = command.split(" ", 1)[1]
        target_player = world_state.players.find_player_by_name(target_player_name)
        if target_player is not None and player.can_telepath():
            await EventUtility.send_message(
                CommandEvent(f'You whisper "{msg}" to {target_player.name}'),
                player.websocket,
            )
            await target_player.websocket.send(
                CommandEvent(f'{player.name} whispers "{msg}" to you.')
            )
        self.logger.debug("exit")
        return player
