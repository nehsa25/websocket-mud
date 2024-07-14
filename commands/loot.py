import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Loot(Utility):
    logger = None
    command = "loot <target>"
    examples = []
    description = "Loot an item from a corpse."
    type = Utility.Share.Commands.LOOT
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Loot() class", self.logger)

    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
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

        if current_monster == None:
            await self.send_message(MudEvents.ErrorEvent(f"{wanted_monster} is not a valid loot target."), player.websocket)
        else:
            if monster.is_alive == True:
                await self.send_message(MudEvents.ErrorEvent(f"You cannot loot {current_monster.name}.  It wouldn't like that."), player.websocket)
            else:
                # take money
                monster_name = current_monster.name.replace("(Dead) ", "")
                if len(current_monster.money) > 0:
                    player.money.extend(current_monster.money)
                    msg = f"You take {len(current_monster.money)} copper from {monster_name}."
                    await self.send_message(MudEvents.InfoEvent(msg), player.websocket)

                    # alert the rest of the room
                    for room_player in world_state.rooms.rooms[player.room.id].players:
                        if room_player.websocket != player.websocket:
                            await self.send_message(MudEvents.InfoEvent(f"{player.name} picks up {len(current_monster.money)} copper from {monster_name}."), room_player.websocket)

                    # remove from monster
                    current_monster.money = 0
                else:
                    await self.send_message(MudEvents.InfoEvent(f"{monster_name} has no money to loot."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player