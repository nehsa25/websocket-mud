from core.data.player_data import PlayerData
from core.enums.commands import CommandEnum
from core.enums.send_scope import SendScopeEnum
from core.events.direction import DirectionEvent
from core.events.error import ErrorEvent
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility


class Move:
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
        "southwest[sw,southw]",
    ]
    description = "Move in a direction."
    type = CommandEnum.MOVE

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Move() class")
        
    async def execute(self, wanted_direction: str, player: PlayerData):
        self.logger.debug("Executing Move command")

        self.logger.debug("enter")

        friendly_direction = await self.world_service.environments.dirs.get_friendly_name(wanted_direction)

        player.room = await self.world_service.get_room(player.room)

        will_travel = False
        new_room_id = None
        for avail_exit in player.room.exits:
            if wanted_direction in avail_exit["direction"].variations:
                will_travel = True
                new_room_id = avail_exit["id"]
                break

        if will_travel:
            # stop resting
            if player.statuses.is_resting:
                await player.set_rest(False)

            # update you
            await DirectionEvent(f"You travel {avail_exit['direction'].name.capitalize()}.").send(player.websocket)

            # Update users you've left
            for p in self.world_service.player_registry.players.players:
                if player.selected_character.name == p.name:
                    continue
                if p.location_id.name == player.room.name:
                    await InfoEvent.send(f"{player.selected_character.name} travels {avail_exit['direction'].name.lower()}.")

            # update location
            player, self.world_service = await self.world_service.move_room_player(new_room_id, player)

            # render new room
            await self.world_service.show_room(player)

            # your combat will end but the monster/other players shouldn't
            if player.in_combat:
                await player.break_combat(self.world_service.rooms.rooms)

            # send message to any players in same room that you're arriving at
            for p in self.world_service.player_registry.players.players:
                if player.selected_character.name == p.name:
                    continue
                if p.location_id.name == player.room.name:
                    opp_direction = avail_exit["direction"].opposite.name
                    await InfoEvent(f"{player.selected_character.name} arrives from the {opp_direction[1].lower()}.").send(
                        player.websocket
                    )
        else:
            await ErrorEvent("You cannot go in that direction.").send(player.websocket)
            await InfoEvent(f"{player.selected_character.name} attempts to go {friendly_direction} but cannot.").send(
                player.websocket, exclude_player=True, scope=SendScopeEnum.ROOM
            )
        self.logger.debug("exit")