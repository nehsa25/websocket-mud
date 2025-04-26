from core.enums.commands import CommandEnum
from core.events.command import CommandEvent
from utilities.events import EventUtility
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

    async def execute(self, command, player, world_state):
        self.logger.debug("enter")
        target_player_name = command.split(" ", 1)[1].split(" ", 1)[0]
        player.room = await world_state.get_room(player.room)
        msg = command.split(" ", 1)[1]
        target_player = world_state.players.find_player_by_name(target_player_name)
        if target_player is not None and target_player.room == player.room:
            await EventUtility.send_message(
                CommandEvent(f'You whisper "{msg}" to {target_player.name}'),
                player.websocket,
            )
            await target_player.websocket.send(
                CommandEvent(f'{player.name} whispers "{msg}" to you.')
            )
        self.logger.debug("exit")
        return player
