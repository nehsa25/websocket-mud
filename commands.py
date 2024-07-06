import inspect
import asyncio
from random import random, randint
import traceback

# my stuff
from aiimages import AIImages
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Commands(Utility):

    class CommandUtility:
        logger = None

        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug(f"Initializing CommandUtility() class", self.logger)

        # returns player, world
        async def drop_item(self, wanted_item, player, world, websocket):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            found_item = False

            # check if it's in our inventory
            item_obj = None
            for item_in_inv in player.inventory.items:
                if wanted_item.lower() == item_in_inv.name.lower():
                    item_obj = item_in_inv
                    found_item = True
                    break

            if found_item == True:
                # set eq'd to False
                item_obj.equiped = False

                # remove from inventory
                player.inventory.items.remove(item_obj)
                await self.world.self.world.utility.send_msg(
                    f"You dropped {item_obj.name}.", "info", websocket, self.logger
                )
                world.rooms.rooms[player.location].append(item_obj)
            return player, world

        # returns player, world
        async def drop_coin(self, wanted_item, player, world, websocket):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            found_coin = False

            # check if it's money
            item_obj = None
            for coin in player.money:
                if wanted_item.lower() == coin.name.lower():
                    item_obj = coin
                    found_coin = True
                    break

            if found_coin == True:
                # add to room
                world.rooms.rooms[player.location].append(item_obj)

                # remove from player inventory
                player.inventory.items.remove(item_obj)
                await self.send_msg(
                    f"You dropped {coin.Name}.", "info", websocket, self.logger
                )
            else:
                await self.send_msg(f"You can't drop {wanted_item}", "error", player.websocket)

            return player, world
    class CommandHelp:
        command = ""
        definition = ""

        def __init__(self, command, definition):
            self.command = command
            self.definition = definition

    logger = None
    command_utility = None
    ai_images = None
    running_image_threads = []

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug(f"Initializing Command() class", self.logger)
        
        if self.ai_images is None:
            self.ai_images = AIImages(self.logger)

        if self.command_utility is None:
            self.command_utility = Commands.CommandUtility(logger)

    # returns nothing, just sends messages
    async def process_help(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        commands = []
        commands.append(Commands.CommandHelp("look[l]", "Look around the room"))
        commands.append(Commands.CommandHelp("get[g]", "Pick up an item"))
        commands.append(Commands.CommandHelp("inventory[inv]", "List your inventory"))
        commands.append(Commands.CommandHelp("drop", "Drop an item"))
        commands.append(Commands.CommandHelp("search[sea]", "Search the room for hidden items"))
        commands.append(Commands.CommandHelp("north[n]", "Move a direction (North[n], South[s], Northwest[nw], Down[d], ect)"))
        commands.append(Commands.CommandHelp("experience[exp]", "Display your experience"))
        commands.append(Commands.CommandHelp("hide", "Hide an item in the room"))
        commands.append(Commands.CommandHelp("stash", "Stash an item in your inventory"))
        commands.append(Commands.CommandHelp("statistics[stat]", "Display your character statistics"))
        commands.append(Commands.CommandHelp("equip", "Equip an item"))
        commands.append(Commands.CommandHelp("attack", "Attack a monster"))
        commands.append(Commands.CommandHelp("loot", "Loot a monster"))
        commands.append(Commands.CommandHelp("who", "List players online"))
        commands.append(Commands.CommandHelp("rest", "Rest to regain health"))
        commands.append(Commands.CommandHelp("say", "Speak to the room"))
        commands.append(Commands.CommandHelp("system name &lt;NEW NAME&gt;", "Change your name"))
        await self.send_message(MudEvents.HelpEvent(commands), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # returns player, world
    async def process_direction(self, wanted_direction, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

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
                if p.location_id == player.room.id:
                    await self.send_message(MudEvents.InfoEvent(f"{player.name} travels {avail_exit['direction'].name.capitalize()}."), p.websocket)

            # update location
            world_state = await world_state.move_room_player(new_room_id, player)

            # render new room
            await world_state.show_room(player, look_location_id=new_room_id)

            # your combat will end but the monster/other players shouldn't
            if player.in_combat:
                await player.break_combat(world_state.rooms.rooms, self.logger)

            # send message to any players in same room that you're arriving at
            for p in world_state.players.players:
                if player.name == p.name:
                    continue
                if p.location_id == player.room.id:
                    opp_direction = None
                    for opp_dir in self.Share.MudDirections.opp_directions:
                        if avail_exit["direction"] == opp_dir[0]:
                            opp_direction = opp_dir[1]
                        if avail_exit["direction"] == opp_dir[1]:
                            opp_direction = opp_dir[0]
                    await self.send_message(MudEvents.InfoEvent(f"{player.name} arrives from the {opp_direction[1].lower()}."), p.websocket)
        else:
            await self.send_message(MudEvents.ErrorEvent(f"You cannot go in that direction."), player.websocket)
            await player.room.alert(f"{player.name} attempted to go {wanted_direction} but ran into a wall!", exclude_player=True, player=player)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world_state

    # doesn't return anything, just sends messages
    async def process_look_direction(self, wanted_direction, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        valid_direction = False
        room = await world_state.get_room(player.room.id)

        # check if it's a valid direction in the room
        for avail_exit in room.exits:
            if wanted_direction in avail_exit["direction"].variations:
                valid_direction = True
                break

        if valid_direction == True:
            await self.send_message(MudEvents.InfoEvent(f"You look to the {avail_exit["direction"].name.capitalize()}."), player.websocket)

            # send message to any players in same room
            for p in world_state.players.players:
                if player.name == p.name:
                    continue
                if p.location_id == player.room.id:
                    await self.send_message(MudEvents.InfoEvent(f"You notice {player.name} looking to the {wanted_direction}."), p.websocket)

            await world_state.show_room(player, look_location_id=avail_exit["id"])
        else:
            for direction in self.Share.MudDirections.pretty_directions:
                if (
                    wanted_direction.lower() == direction[0].lower()
                    or wanted_direction.lower() == direction[1].lower()
                ):
                    await self.send_message(MudEvents.ErrorEvent(f"{direction[1]} is not a valid direction to look."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # doesn't return anything, just sends messages
    async def process_look(self, look_object, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, direction: {look_object}", self.logger)
        found = False
        if len(look_object.split(" ", 1)) > 1:
            look_object = look_object.split(" ", 1)[1].lower()

        # do we just want to look around the room?
        if look_object == "l" or look_object == "look":
            found = True
            await self.send_message(MudEvents.InfoEvent("You look around the room."), player.websocket)
            await world_state.show_room(player)

            # send message to any players in same room that you're being suspicious
            await player.room.alert(f"You notice {player.name} gazing around the room.", exclude_player=True, player=player, event_type=MudEvents.InfoEvent)
            if found: return

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
                        type=Utility.Share.ImageType.PLAYER
                    )
                )
            )
            
            msg = await player.get_player_description()
            await self.send_message(
                MudEvents.RestEvent(msg, is_resting=False),
                player.websocket,
            )
            if found: return

        # are we looking at a player?
        if player.room.players != None:
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
                                type=Utility.Share.ImageType.PLAYER
                            )
                        )
                    )
                    await self.send_message(MudEvents.InfoEvent(await p.get_player_description()), player.websocket)
                    break
            if found: return
                
        # are we looking at a npc?
        if player.room.npcs != None:
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
                                type=Utility.Share.ImageType.NPC
                            )
                        )
                    )
                    await self.send_message(MudEvents.InfoEvent(npc.description), player.websocket)
                    break
            if found: return
                
        # are we looking at a monster?
        if player.room.monsters != None:
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
                                type=Utility.Share.ImageType.MONSTER
                            )
                        )
                    )
                    await self.send_message(MudEvents.InfoEvent(monster.description), player.websocket)
                    break
            if found: return
                
        # are we looking at a item?
        if player.room.items != None:
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
                                type=Utility.Share.ImageType.ITEM
                            )
                        )
                    )
                    await self.send_message(MudEvents.InfoEvent(item.description), player.websocket)
                    break
            if found: return

        if not found:
            await self.send_message(MudEvents.ErrorEvent(f"You don't notice anything."), player.websocket)

        LogUtils.debug(f"{method_name}: exit", self.logger)

    # returns player, world
    async def process_get(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1].lower()
        found_item = False

        for item in player.room.items:
            if wanted_item == item.name.lower():
                found_item = True
                await self.send_message(MudEvents.InfoEvent(f"You pick up {item.name}."), player.websocket)

                # remove from room
                player.room.items.remove(item)

                # alert the rest of the room
                await player.room.alert(f"{player.name} picks up {item.name}.", exclude_player=True, player=player, event_type=MudEvents.InfoEvent)

                # add to our inventory
                player.inventory.items.append(item)
                break
        if found_item == False:
            await self.send_message(MudEvents.ErrorEvent(f"You cannot find {wanted_item}."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world_state

    # doesn't return anything, just sends messages
    async def process_inventory(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await player.send_inventory()
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # doesn't return anything, just sends messages
    async def process_search(self, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        rand = random()
        success = rand < (player.stats.perception / 100)
        if success == True:
            if len(world_state.rooms.rooms[player.room.id].hidden_items) > 0:
                for item in world_state.rooms.rooms[player.room.id].hidden_items:
                    await self.send_message(MudEvents.InfoEvent(f"You found {item.name}!"), player.websocket)

                    # remove from "hidden items"
                    world_state.rooms.rooms[player.room.id].hidden_items.remove(item)

                    # add to items in room
                    world_state.rooms.rooms[player.room.id].items.append(item)
            else:
                await self.send_message(MudEvents.InfoEvent("After an exhaustive search, you find nothing and give up."), player.websocket)
        else:
            await self.send_message(MudEvents.InfoEvent("You search around but notice nothing."), player.websocket)

        LogUtils.info(f"{method_name}: player {player.name} search yielded results: {success}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # returns player, world
    async def process_drop(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1]
        player, world_state = await self.command_utility.drop_item(
            wanted_item, player, world_state
        )
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world_state

    async def process_hide_item(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1]
        found_item = False

        # check if it's in our inventory
        item_obj = None
        for item_in_inv in player.items.inventory:
            if wanted_item.lower() == item_in_inv.name.lower():
                item_obj = item_in_inv
                found_item = True
                break

        if found_item == True:
            # remove from inventory
            player.inventory.items.remove(item_obj)
            await self.send_message(MudEvents.InfoEvent(f"You hid {item_obj.name}."), player.websocket)
            world_state.rooms.rooms[player.room.id].hidden_items.append(item_obj)
        else:
            await self.send_message(MudEvents.ErrorEvent(f"You aren't carrying {wanted_item} to hide."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player

    async def process_equip_item(self, command, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1]
        found_item = None

        # check if the item is in our inventory
        for item in player.inventory.items:
            if item.name.lower() == wanted_item.lower():
                await self.send_message(MudEvents.InfoEvent(f"You equip {item.name}."), player.websocket)
                item.equiped = True
                found_item = True
                found_item = item

        # if you eq'd an item, deselect any previous items
        for item in player.inventory.items:
            if (
                found_item.item_type == item.item_type and item.equiped == True
            ) and found_item.name != item.name:
                await self.send_message(f"You unequip {item.name}.", "info", player.websocket)
                item.equiped = False
        if found_item == None:
            await self.send_message(f"You cannot equip {wanted_item}.", "error", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player

    async def process_system_command(self, command, extra, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_command = command.split(" ")
        subcmd = None
        request = None
        if len(wanted_command) == 3:
            subcmd = wanted_command[1]
            request = wanted_command[2].capitalize()

        if subcmd == "name":
            player.name = request

            # check if user already in system (they should be)
            world_state = await world_state.players.unregister(player, world_state, change_name=True)
            player, world_state = await world_state.players.register(player, world_state)
            await self.send_message(MudEvents.InfoEvent(f"You are now known as {player.name}"), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player

    async def process_stat(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        player_stats = f"""        
        Hello {player.name}<br>
        **************************************************<br>
        Level: {player.level}<br>
        Experience: {player.experience}<br>
        **************************************************<br>
        Race: {player.race.name}<br>
        Class: {player.player_class.name}<br>
        **************************************************<br>
        You have the following attributes:<br>
        * Health {player.stats.current_hp} of {player.stats.max_hp}<br>
        * Strength {player.stats.strength}<br>
        * Agility {player.stats.agility}<br>
        * Determination {player.stats.determination}<br>
        * Faith {player.stats.faith}<br>
        * Intelligence {player.stats.intelligence}<br>
        * Perception {player.stats.perception}<br>
        Current Conditions and Aielments:<br>
        * Feriocity {player.stats.feriocity.name.capitalize()}<br>
        * Resting {player.stats.is_resting}<br>
        * Poisoned {player.stats.is_posioned}<br>
        **************************************************<br>
        """
        await self.send_message(MudEvents.InfoEvent(player_stats), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player

    async def process_exp(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await self.send_message(MudEvents.InfoEvent(f"You have {player.experience} experience."), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player

    async def process_attack_mob(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        room = world_state.rooms.rooms[player.room.id]

        # att skeleton
        wanted_monster = command.split(" ", 1)[1].lower()  # wanted_monster == skeleton

        # see if this monster is in the room.
        current_monster = None
        room_monsters = room.monsters
        for monster in room_monsters:
            monster_name = monster.name.lower().strip()
            monster_name_parts = monster_name.split(" ")
            for name in monster_name_parts:
                if name.startswith(wanted_monster) and monster.is_alive == True:
                    current_monster = monster
                    break

        if current_monster != None:
            if player.in_combat == None:
                for p in world_state.rooms.rooms[player.room.id].players:
                    if p.name == player.name:
                        await self.send_message(MudEvents.InfoEvent(f"You begin to attack {current_monster.name}!"), p.websocket)
                        p.in_combat = current_monster
                    else:
                        await self.send_message(MudEvents.InfoEvent(f"{player.name} begins to attack {current_monster.name}!"), p.websocket)

                # if you die and go to the crypt then your room id will change..
                while current_monster.hitpoints > 0 and player.room.id == world_state.rooms.rooms[player.room.id].id:
                    # determine attack damage
                    attack_potential = player.weapon.damage_potential

                    # for number of swings here
                    num_swings = 1
                    num_swings += int(player.stats.agility / player.weapon.weight_class.value)

                    LogUtils.debug(f"We're going to swing {num_swings} times!", self.logger)

                    damage = 0
                    for x in range(0, num_swings):
                        LogUtils.debug(f"Swinging!", self.logger)
                        # attack monster
                        obj = attack_potential.split(
                            "d"
                        )  # obj = obj[0] == 1, obj[1] == 2
                        dice = int(obj[0])  # 1
                        damage_potential = int(obj[1])  # 2
                        damage_multipler = randint(0, damage_potential)
                        damage += dice * damage_multipler * player.stats.strength

                    for p in world_state.rooms.rooms[player.room.id].players:
                        response = ""
                        if player.name == p.name:
                            if damage == 0:
                                response = f"You swing wildly and miss!"
                            else:
                                if num_swings == 1:
                                    response = f"You {player.weapon.verb} {current_monster.name} with your {player.weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"You {player.weapon.verb} {current_monster.name} {num_swings} times with your {player.weapon.name.lower()} for {str(damage)} damage!"
                                await self.send_message(MudEvents.InfoEvent(response), p.websocket)
                        else:
                            if damage == 0:
                                response = f"{player.name} swings wildly and misses!"
                            else:
                                if num_swings == 1:
                                    response = f"{player.name} {player.weapon.plural_verb} {current_monster.name} with their {player.weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"{player.name} {player.weapon.plural_verb} {current_monster.name} {num_swings} times with their {player.weapon.name.lower()} for {str(damage)} damage!"
                                await self.send_message(MudEvents.InfoEvent(response), p.websocket)

                    # subtract from monsters health
                    current_monster.hitpoints = current_monster.hitpoints - damage

                    if current_monster.hitpoints <= 0:
                        # set monster as dead
                        await current_monster.kill(world_state.rooms.rooms[player.room.id], self.logger)

                        for p in world_state.rooms.rooms[player.room.id].players:
                            if p.in_combat == current_monster:
                                # give experience
                                p.experience += current_monster.experience

                                # send defeat message
                                msg = f"You vanquished {current_monster.name}!<br>You received {current_monster.experience} experience."
                                await self.send_message(MudEvents.InfoEvent(msg), p.websocket)

                                # set combat back to none so we can fight someone else
                                p.in_combat = None

                                # show room
                                await world_state.show_room(player)

                        # add (Dead) to monster
                        current_monster.name = f"{current_monster.name} (Dead)"
                    else:
                        await asyncio.sleep(3)
            else:
                await self.send_message(MudEvents.ErrorEvent(f"You cannot attack {current_monster.name}.  You are already in combat with {player.in_combat.name}."), player.websocket)
        else:
            await self.send_message(MudEvents.ErrorEvent(f"{wanted_monster} is not a valid attack target."), player.websocket)
        world_state.rooms.rooms[player.room.id].monsters = room_monsters
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player

    async def process_loot(self, command, player, world_state):
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

    async def process_who(self, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        players = ""
        for player in world_state.players.players:
            players += f"{player.name}<br>"

        await self.send_message(MudEvents.AnnouncementEvent(f"Players Online:<br>{players}"), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player

    async def process_comms(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if command.startswith("/say "):
            msg = command.split(" ", 1)[1]
            for p in world_state.players.players:
                if p.name == player.name:
                    await self.send_message(MudEvents.CommandEvent(f'You say "{msg}"'), p.websocket)
                else:
                    await self.send_message(MudEvents.CommandEvent(f'{player.name} says "{msg}"'), p.websocket)

        # elif command.startswith('/yell '): # can be heard from ajoining rooms
        #     pass
        # else: # it's a telepath
        #     pass
        LogUtils.debug(f"{method_name}: exit")
        return player

    async def process_rest(self, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        monsters_in_room = len(player.room.monsters)
        if player.in_combat == True or monsters_in_room > 0:
            player.stats.is_resting = False
            await self.send_message(MudEvents.RestEvent("You cannot rest at this time.  You are in combat.", rest_error=True, is_resting=False), player.websocket)
        else:
            # message staying you're starting to rest
            await self.send_message(MudEvents.RestEvent("You settle to rest.", rest_error=False, is_resting=True), player.websocket)

            # set an attribute that we can use later
            player.stats.is_resting = True

        # press enter (refresh the room)
        await world_state.show_room(player)

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return  player, world_state

    # main function that runs all the rest
    async def run_command(self, command, player, world_state, extra = ""):
        try:
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            LogUtils.debug(f'Command: "{command}"', self.logger)
            command = command.lower()

            # send back the command we received as info - (this could just be printed client side and save the traffic cost)
            await self.send_message(MudEvents.CommandEvent(command), player.websocket)

            # if the player is dead, don't do anything..
            if player.stats.current_hp <= 0:
                return player

            # process each command
            if command == "":
                await world_state.show_room(player)
            elif command == "help":  # display help
                player = await self.process_help(player)
            elif world_state.environments.dirs.is_valid_direction(command):  # process direction
                player = await self.process_direction(command, player, world_state)
            # a look command - could be at the room, a person, a monster, an item
            elif command == "l" or command == "look" or command.startswith("l ") or command.startswith("look "):
                player = await self.process_look(command, player, world_state)
            elif command.startswith("g ") or command.startswith("get "):  # get
                player = await self.process_get(command, player, world_state)
            elif command == "i" or command == "inv" or command == "inventory":  # inv
                player = await self.process_inventory(player)
            elif command == "sea" or command == "search":  # search
                player = await self.process_search(player, world_state)
            elif command.startswith("dr ") or command.startswith("drop "):  # drop
                player = await self.process_drop(command, player)
            elif command.startswith("hide ") or command.startswith("stash "):  # hide
                player = await self.process_hide_item(command, player, world_state)
            elif command.startswith("eq ") or command.startswith("equip "):  # eq
                player = await self.process_equip_item(command, player)
            elif command.startswith("system "):  # a system command like changing username
                player = await self.process_system_command(command, extra, player, world_state)
            elif command == "stat":  # stat
                player = await self.process_stat(player)
            elif (command.startswith("a ")  or command.startswith("att ") or command.startswith("attack ")):  # attack
                asyncio.create_task(
                    self.process_attack_mob(command, player, world_state)
                )
            elif command == ("exp") or command == ("experience"):  # experience
                player = await self.process_exp(player)
            elif command.startswith("loot "):  # loot corpse
                player = await self.process_loot(command, player, world_state)
            elif command == ("who"):
                player = await self.process_who(player, world_state)
            elif command.startswith("/"):
                player = await self.process_comms(command, player, world_state)
            elif command == "rest":
                player, world_state = await self.process_rest(player, world_state)
            else:  # you're going to say it to the room..
                await self.send_message(MudEvents.ErrorEvent(f'"{command}" is not a valid command.'), player.websocket)

            LogUtils.debug(f"{method_name}: exit", self.logger)
            return player
        except:
            LogUtils.error(f"{method_name}: An error occurred executing command: {command} from player {player.name}\n---------\n{traceback.format_exc()}", self.logger)
            