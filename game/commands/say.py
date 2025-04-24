from game.enums.commands import Commands
from game.events.command import CommandEvent
from game.events.info import InfoEvent
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class Say:
    logger = None
    command = "say <message>"
    examples = ["say 'sup homies?"]
    description = "Say something to the room you're in."
    type = Commands.SAY

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Say() class")

    async def execute(self, command, player, world_state):
        self.logger.debug("enter")
        player.room = await world_state.get_room(player.room)
        msg = command.split(" ", 1)[1]
        await EventUtility.send_message(
            CommandEvent(f'You say "{msg}"'), player.websocket
        )
        await player.room.alert(
            f'{player.name} says "{msg}"',
            exclude_player=True,
            player=player,
            event_type=InfoEvent,
        )
        self.logger.debug("exit")
        return player
