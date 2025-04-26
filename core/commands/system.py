from core.enums.commands import CommandEnum
from core.events.error import ErrorEvent
from utilities.events import EventUtility
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

    async def execute(self, command, extra, player, world_state):
        self.logger.debug("enter")
        wanted_command = command.split(" ")
        action_to_take = None
        request = None
        if len(wanted_command) < 1:
            await EventUtility.send_message(
                ErrorEvent("Invalid system command"), player.websocket
            )
            return player

        # this is the acton component of the command
        action_to_take = wanted_command[1]

        if action_to_take == "name":
            if len(wanted_command) == 3 or extra:
                request = wanted_command[2].capitalize()

            player.name = request

            # check if user already in system (they should be)
            world_state = await world_state.players.unregister(
                player, world_state, change_name=True
            )
            player, world_state = await world_state.players.register(
                player, world_state
            )
            await EventUtility.send_message(
                EventUtility.UsernameChangedEvent(
                    f"You are now known as {player.name}", player.name
                ),
                player.websocket,
            )
        self.logger.debug("exit")
        return player
