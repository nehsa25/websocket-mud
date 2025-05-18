from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.events.error import ErrorEvent
from core.events.username_change import UsernameChangedEvent
from utilities.log_telemetry import LogTelemetryUtility


class System:
    logger = None
    command = "system <subcommand> <args>"
    examples = [
        "system name Hopper - change your name to Hopper",
        "sys name Kvothe",
        "sys name - open change name modal",
    ]
    description = "Perform a system command"
    type = CommandEnum.SYSTEM

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing System() class")

    async def execute(self, command: str, extra: str, player: PlayerData):
        self.logger.debug("enter")
        wanted_command = command.split(" ")
        action_to_take = None
        request = None
        if len(wanted_command) < 1:
            await ErrorEvent("Invalid system command").send(player.websocket)
            return player

        # this is the acton component of the command
        action_to_take = wanted_command[1]

        if action_to_take == "name":
            if len(wanted_command) == 3 or extra:
                request = wanted_command[2].capitalize()

            player.selected_character.name = request

            # check if user already in system (they should be)
            self.world_service = await self.world_service.player_registry.players.unregister(
                player, self.world_service, change_name=True
            )
            player, self.world_service = await self.world_service.player_registry.players.register(
                player, self.world_service
            )
            await UsernameChangedEvent(
                    f"You are now known as {player.selected_character.name}", player.selected_character.name
                ).send(player.websocket)
        self.logger.debug("exit")
