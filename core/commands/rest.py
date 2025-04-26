from core.enums.commands import CommandEnum
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class Rest:
    logger = None
    command = "rest"
    examples = ["rest"]
    description = "Rest and regain your health."
    type = CommandEnum.REST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Rest() class")

    async def execute(self, player, world_state):
        self.logger.debug("enter")
        monsters_in_room = len(player.room.monsters)
        if player.in_combat is True or monsters_in_room > 0:
            player.statuses.is_resting = False
            await EventUtility.send_message(
                EventUtility.RestEvent(
                    "You cannot rest at this time.  You are in combat.",
                    rest_error=True,
                    is_resting=False,
                ),
                player.websocket,
            )
        else:
            # message staying you're starting to rest
            await EventUtility.send_message(
                EventUtility.RestEvent(
                    "You settle to rest.", rest_error=False, is_resting=True
                ),
                player.websocket,
            )

            # set an attribute that we can use later
            player.statuses.is_resting = True

        # press enter (refresh the room)
        await world_state.show_room(player)

        self.logger.debug("exit")
        return player, world_state
