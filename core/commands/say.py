from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.enums.send_scope import SendScopeEnum
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility


class Say:
    logger = None
    command = "say <message>"
    examples = ["say 'sup homies?"]
    description = "Say something to the room you're in."
    type = CommandEnum.SAY

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Say() class")
        
    async def execute(self, command: str, player: PlayerData):
        self.logger.debug("enter")
        player.room = await self.world_service.get_room(player.room)
        msg = command.split(" ", 1)[1]
        await InfoEvent(f'You say "{msg}"').send(player.websocket)
        await InfoEvent(f'{player.selected_character.name} says "{msg}"').send(
            player.websocket, exclude_player=True, scope=SendScopeEnum.ROOM
        )
        self.logger.debug("exit")
