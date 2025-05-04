from core.enums.commands import CommandEnum
from core.events.error import ErrorEvent
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility


class Loot:
    logger = None
    command = "loot <target>"
    examples = [
        "loot skeleton",
    ]
    description = "Loot from corpses"
    type = CommandEnum.LOOT

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Loot() class")

    async def execute(self, command, player, world_state):
        self.logger.debug("enter")
        wanted_monster = command.split(" ", 1)[1]  # loot skeleton

        # see if this monster is in the room.
        current_monster = None
        for monster in world_state.rooms.rooms[player.room.id].monsters:
            monster_name = monster.name.lower().strip()
            monster_name_parts = monster_name.split(" ")
            for name in monster_name_parts:
                if name.startswith(wanted_monster):
                    current_monster = monster
                    break

        if current_monster is None:
            await ErrorEvent(f"{wanted_monster} is not a valid loot target.").send(player.websocket)
        else:
            if monster.is_alive is True:
                await ErrorEvent(f"You cannot loot {current_monster.name}.  It wouldn't like that.").send(
                    player.websocket
                )
            else:
                # take money
                monster_name = current_monster.name.replace("(Dead) ", "")
                if len(current_monster.money) > 0:
                    player.money.extend(current_monster.money)
                    msg = f"You take {len(current_monster.money)} copper from {monster_name}."
                    await InfoEvent(msg).send(player.websocket)

                    # alert the rest of the room
                    for room_player in world_state.rooms.rooms[player.room.id].players:
                        if room_player.websocket != player.websocket:
                            await InfoEvent(
                                f"{player.name} picks up {len(current_monster.money)} copper from {monster_name}."
                            ).send(room_player.websocket)

                    # remove from monster
                    current_monster.money = 0
                else:
                    await InfoEvent(f"{monster_name} has no money to loot.").send(player.websocket)
        self.logger.debug("exit")
        return player
