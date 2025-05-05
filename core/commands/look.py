import asyncio
from core.enums.images import ImageEnum
from core.enums.send_scope import SendScopeEnum
from core.events.error import ErrorEvent
from core.events.info import InfoEvent
from services.ai.image import AIImages
from utilities.log_telemetry import LogTelemetryUtility
from core.enums.commands import CommandEnum


class Look:
    ai_images = None
    logger = None
    command = "look, look <target>"
    examples = [
        "l - look around the room",
        "l sword - look at a sword",
        "look bink - look at a player named Bink",
        "l n - look north",
    ]
    description = "Look at something."
    running_image_threads = []
    type = CommandEnum.LOOK

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Look() class")

        if self.ai_images is None:
            self.ai_images = AIImages()

    async def process_look_direction(self, wanted_direction, player, world_state):
        self.logger.debug("enter")
        valid_direction = False

        player.room = await world_state.get_room(player.room)

        # check if it's a valid direction in the room
        for avail_exit in player.room.exits:
            if wanted_direction in avail_exit["direction"].variations:
                valid_direction = True
                break

        if valid_direction is True:
            await InfoEvent(
                f"{player.name} looks to the {wanted_direction}.", player.room.id
            ).send(player.websocket)

            # send message to any players in same room
            for p in world_state.players.players:
                if player.name == p.name:
                    continue
                if p.location_id.name == player.room.name:
                    await InfoEvent(
                        f"{player.name} looks to the {wanted_direction}.", p.websocket
                    ).send(p.websocket)

            await world_state.show_room(player, look_location_room=avail_exit["id"])
        else:
            for direction in self.Share.MudDirections.pretty_directions:
                if (wanted_direction.lower() == direction[0].lower() or wanted_direction.lower() == direction[1].lower()):
                    await ErrorEvent(
                        f"'{wanted_direction}' is not a valid direction to look."
                    ).send(player.websocket)
        self.logger.debug("exit")

    async def execute(self, look_object, player, world_state):
        self.logger.debug("Executing Look command")

        self.logger.debug(f"enter, direction: {look_object}")

        player.room = await world_state.get_room(
            player.location_id
        )  # Use player.location

        # do we just want to look around the room?
        if look_object == "" or look_object == "l" or look_object == "look":
            room = await world_state.show_room(player)
            self.running_image_threads.append(
                asyncio.create_task(
                    self.ai_images.generate_image(
                        item_name=self.sanitize_filename(f"{player.room.name}_room") + ".png",
                        item_description=room.description,
                        player=player,
                        world_state=world_state,
                        type=ImageEnum.ROOM,
                    )
                )
            )
            await InfoEvent("You look around the room.").send(player.websocket)

            # send message to any players in same room that you're being suspicious
            await InfoEvent(f"You notice {player.name} gazing around the room.").send(
                    player.websocket,
                    scope=SendScopeEnum.ROOM,
                    exclude_player=True
                )
            
        elif len(look_object.split(" ", 1)) > 1:
            found = False
            look_object = look_object.split(" ", 1)[1].lower()

            # are we looking in a direction?
            if world_state.environments.dirs.is_valid_direction(look_object):
                found = True
                await self.process_look_direction(look_object, player, world_state)
                if found:
                    return

            # are we looking at ourselve?
            if look_object in player.name.lower():
                found = True
                player_description = await player.get_player_description()

                self.running_image_threads.append(
                    asyncio.create_task(
                        self.ai_images.generate_image(
                            item_name=self.create_unique_name(f"{player.name}_player") + ".png",
                            item_description=player_description,
                            player=player,
                            world_state=world_state,
                            type=ImageEnum.PLAYER,
                        )
                    )
                )

                msg = await player.get_player_description()
                await InfoEvent(msg).send(player.websocket)
                if found:
                    return

            # are we looking at a player?
            if (player.room and player.room.players is not None and player.room.players != []):  # Check if player.room exists
                for p in player.room.players:
                    if look_object in p.name.lower():
                        found = True
                        description = await p.get_player_description()
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(
                                        f"{player.name}_player"
                                    ) + ".png",
                                    item_description=description,
                                    player=player,
                                    world_state=world_state,
                                    type=ImageEnum.PLAYER,
                                )
                            )
                        )
                        InfoEvent(await p.get_player_description()).send(player.websocket)
                        break
                if found:
                    return

            # are we looking at a npc?
            if (
                player.room and player.room.npcs is not None
            ):  # Check if player.room exists
                for npc in player.room.npcs:
                    if (
                        look_object in npc.name.lower() or look_object in npc.title.lower()
                    ):
                        found = True
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(
                                        f"{player.name}_npc"
                                    ) + ".png",
                                    item_description=npc.description,
                                    player=player,
                                    world_state=world_state,
                                    type=ImageEnum.NPC,
                                )
                            )
                        )
                        await InfoEvent(
                            f"{player.name} looks at {npc.name}."
                        ).send(player.websocket)
                        break
                if found:
                    return

            # are we looking at a monster?
            if (
                player.room and player.room.monsters is not None
            ):  # Check if player.room exists
                for monster in player.room.monsters:
                    if look_object in monster.name.lower():
                        found = True
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(
                                        f"{player.name}_monster"
                                    ) + ".png",
                                    item_description=monster.description,
                                    player=player,
                                    world_state=world_state,
                                    type=ImageEnum.MONSTER,
                                )
                            )
                        )
                        await InfoEvent(monster.description).send(player.websocket)
                        break
                if found:
                    return

            # are we looking at a item?
            if player.room and player.room.items is not None:
                for item in player.room.items:
                    if look_object in item.name.lower():
                        found = True
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(
                                        f"{player.name}_item"
                                    ) + ".png",
                                    item_description=item.description,
                                    player=player,
                                    world_state=world_state,
                                    type=ImageEnum.ITEM,
                                )
                            )
                        )
                        await InfoEvent(item.description).send(player.websocket) 
                        break
                if found:
                    return

            if not found:
                await ErrorEvent("You don't notice anything.").send(player.websocket)

        self.logger.debug("exit")
