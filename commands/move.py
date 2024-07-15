from copy import deepcopy
import inspect
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Move(Utility):
    logger = None
    command = "<direction>"
    examples = [
        "north[n, nor]", 
        "south[s, sou]", 
        "east[e]", 
        "west[w]", 
        "up[u]", 
        "down[d]", 
        "northeast[ne, northe]", 
        "northwest[nw, northw]", 
        "southeast[se,southe]", 
        "southwest[sw,southw]"
    ]
    description = "Move in a direction."
    type = Utility.Share.Commands.MOVE
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Move() class", self.logger)

    async def execute(self, wanted_direction, player, world_state):
        LogUtils.debug("Executing Move command", self.logger)
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        friendly_direction = await world_state.environments.dirs.get_friendly_name(wanted_direction)
        
        player.room = await world_state.get_room(player.room)

        will_travel = False
        new_room_id = None
        for avail_exit in player.room.exits:
            if wanted_direction in avail_exit["direction"].variations:
                will_travel = True
                new_room_id = avail_exit["id"]
                break

        if will_travel:
            # stop resting
            if player.stats.is_resting:
                await player.set_rest(False)

            # update you
            await self.send_message(MudEvents.DirectionEvent(f"You travel {avail_exit['direction'].name.capitalize()}."), player.websocket)

            # Update users you've left
            for p in world_state.players.players:
                if player.name == p.name:
                    continue
                if p.location_id.name == player.room.name:
                    await self.send_message(MudEvents.InfoEvent(f"{player.name} travels {avail_exit['direction'].name.lower()}."), p.websocket)

            # update location
            player, world_state = await world_state.move_room_player(new_room_id, player)

            # render new room
            await world_state.show_room(player)

            # your combat will end but the monster/other players shouldn't
            if player.in_combat:
                await player.break_combat(world_state.rooms.rooms, self.logger)

            # send message to any players in same room that you're arriving at
            for p in world_state.players.players:
                if player.name == p.name:
                    continue
                if p.location_id.name == player.room.name:
                    opp_direction = avail_exit['direction'].opposite.name
                    await self.send_message(MudEvents.InfoEvent(f"{player.name} arrives from the {opp_direction[1].lower()}."), p.websocket)
        else:
            await self.send_message(MudEvents.ErrorEvent(f"You cannot go in that direction."), player.websocket)
            await player.room.alert(f"{player.name} attempted to go {friendly_direction} but could not!", exclude_player=True, player=player)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world_state