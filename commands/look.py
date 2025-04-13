import asyncio
import inspect
from ai.image import AIImages
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Look(Utility):
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
    type = Utility.Commands.LOOK
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Look() class", self.logger)
        
        if self.ai_images is None:
            self.ai_images = AIImages(self.logger)


    async def process_look_direction(self, wanted_direction, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        valid_direction = False
        
        player.room = await world_state.get_room(player.room)

        # check if it's a valid direction in the room
        for avail_exit in player.room.exits:
            if wanted_direction in avail_exit["direction"].variations:
                valid_direction = True
                break

        if valid_direction == True:
            await self.send_message(MudEvents.InfoEvent(f"You look to the {avail_exit["direction"].name.capitalize()}."), player.websocket)

            # send message to any players in same room
            for p in world_state.players.players:
                if player.name == p.name:
                    continue
                if p.location_id.name == player.room.name:
                    await self.send_message(MudEvents.InfoEvent(f"You notice {player.name} looking to the {wanted_direction}."), p.websocket)

            await world_state.show_room(player, look_location_room=avail_exit["id"])
        else:
            for direction in self.Share.MudDirections.pretty_directions:
                if (
                    wanted_direction.lower() == direction[0].lower()
                    or wanted_direction.lower() == direction[1].lower()
                ):
                    await self.send_message(MudEvents.ErrorEvent(f"{direction[1]} is not a valid direction to look."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def execute(self, look_object, player, world_state):
        LogUtils.debug("Executing Look command", self.logger)
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, direction: {look_object}", self.logger)

        player.room = await world_state.get_room(player.location_id) # Use player.location

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
                        type=Utility.ImageType.ROOM
                    )
                )
            )
            await self.send_message(MudEvents.InfoEvent("You look around the room."), player.websocket)


            # send message to any players in same room that you're being suspicious
            if player.room: # Check if player.room exists
                await player.room.alert(f"You notice {player.name} gazing around the room.", exclude_player=True, player=player, event_type=MudEvents.InfoEvent)
        elif len(look_object.split(" ", 1)) > 1:
            found = False
            look_object = look_object.split(" ", 1)[1].lower()

            # are we looking in a direction?
            if world_state.environments.dirs.is_valid_direction(look_object):
                found = True
                await self.process_look_direction(look_object, player, world_state)
                if found: return

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
                            type=Utility.ImageType.PLAYER
                        )
                    )
                )

                msg = await player.get_player_description()
                await self.send_message(
                    MudEvents.InfoEvent(msg),
                    player.websocket,
                )
                if found: return

            # are we looking at a player?
            if player.room and player.room.players != None and player.room.players != []: # Check if player.room exists
                for p in player.room.players:
                    if look_object in p.name.lower():
                        found = True
                        description = await p.get_player_description()                    
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(f"{player.name}_player") + ".png",
                                    item_description=description,
                                    player=player,
                                    world_state=world_state,
                                    type=Utility.ImageType.PLAYER
                                )
                            )
                        )
                        await self.send_message(MudEvents.InfoEvent(await p.get_player_description()), player.websocket)
                        break
                if found: return

            # are we looking at a npc?
            if player.room and player.room.npcs != None: # Check if player.room exists
                for npc in player.room.npcs:
                    if look_object in npc.name.lower() or look_object in npc.title.lower():
                        found = True
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(f"{player.name}_npc") + ".png",
                                    item_description=npc.description,
                                    player=player,
                                    world_state=world_state,
                                    type=Utility.ImageType.NPC
                                )
                            )
                        )
                        await self.send_message(MudEvents.InfoEvent(npc.description), player.websocket)
                        break
                if found: return

            # are we looking at a monster?
            if player.room and player.room.monsters != None: # Check if player.room exists
                for monster in player.room.monsters:
                    if look_object in monster.name.lower():
                        found = True
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(f"{player.name}_monster") + ".png",
                                    item_description=monster.description,
                                    player=player,
                                    world_state=world_state,
                                    type=Utility.ImageType.MONSTER
                                )
                            )
                        )
                        await self.send_message(MudEvents.InfoEvent(monster.description), player.websocket)
                        break
                if found: return

            # are we looking at a item?
            if player.room and player.room.items != None: # Check if player.room exists
                for item in player.room.items:
                    if look_object in item.name.lower():
                        found = True
                        self.running_image_threads.append(
                            asyncio.create_task(
                                self.ai_images.generate_image(
                                    item_name=self.create_unique_name(f"{player.name}_item") + ".png",
                                    item_description=item.description,
                                    player=player,
                                    world_state=world_state,
                                    type=Utility.ImageType.ITEM
                                )
                            )
                        )
                        await self.send_message(MudEvents.InfoEvent(item.description), player.websocket)
                        break
                if found: return

            if not found:
                await self.send_message(MudEvents.ErrorEvent(f"You don't notice anything."), player.websocket)

        LogUtils.debug(f"{method_name}: exit", self.logger)
