import inspect
import asyncio
from random import random, randint

# my stuff
from command_utility import CommandUtility
from log_utils import LogUtils
from muddirections import MudDirections
from mudevent import MudEvents
from utility import Utility

class Command(Utility):
    logger = None
    command_utility = None

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug(f"Initializing Command() class", self.logger)

        if self.command_utility is None:
            self.command_utility = CommandUtility(logger)


    # returns nothing, just sends messages
    async def process_help(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        help_msg = "look, get, inventory, drop, search, hide, stash, equip"
        await self.send_msg(help_msg, "info", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 

    # returns player, world
    async def process_direction(self, wanted_direction, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   

        will_travel = False
        new_room_id = None
        for avail_exit in world.rooms.rooms[player.location_id].exits:
            if (wanted_direction == avail_exit["direction"][0].lower() or wanted_direction == avail_exit["direction"][1].lower()):
                will_travel = True
                new_room_id = avail_exit["id"]
                break
            
        if will_travel:
            # update you
            await self.send_message(MudEvents.DirectionEvent(f"You travel {avail_exit['direction'][1].lower()}."), player.websocket)
            
            # Update users you've left
            for p in world.players.players:
                if player.name == p.name:
                    continue
                if p.location_id == player.location_id:
                    await self.send_message(MudEvents.InfoEvent(f"{player.name} travels {avail_exit['direction'][1].lower()}."), p.websocket)

            # update location
            player, world = await world.rooms.move_room(new_room_id, player, world)

            # render new room
            await world.rooms.process_room(player.location_id, player, world)
            
            # your combat will end but the monster/other players shouldn't
            if player.in_combat:
                await player.break_combat()
            
            # stop resting
            if player.resting:
                player.stop_resting()

            # send message to any players in same room that you're arriving at
            for p in world.players.players:
                if player.name == p.name:
                    continue
                if p.location_id == player.location_id:
                    opp_direction = None
                    for opp_dir in MudDirections.opp_directions:
                        if avail_exit["direction"] == opp_dir[0]:
                            opp_direction = opp_dir[1]
                        if avail_exit["direction"] == opp_dir[1]:
                            opp_direction = opp_dir[0]
                    await self.send_message(MudEvents.InfoEvent(f"{player.name} arrives from the {opp_direction[1].lower()}."), p.websocket)
        else:
            await self.send_message(MudEvents.ErrorEvent(f"You cannot go in that direction."), player.websocket)
            self.alert_room(world, f"{player.name} attempted to go {wanted_direction} but ran into a wall!")
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player, world

    # doesn't return anything, just sends messages
    async def process_look_direction(self, command, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        wanted_direction = command.split(" ", 1)[1].lower()
        valid_direction = False

        # check if it's a valid direction in the room
        for avail_exit in world.rooms.rooms[player.location_id].exits:
            if (
                wanted_direction == avail_exit["direction"][0].lower()
                or wanted_direction == avail_exit["direction"][1].lower()
            ):
                valid_direction = True
                break

        if valid_direction == True:
            await self.send_msg(f"You look to the {avail_exit['direction'][1]}","info", player.websocket)

            # send message to any players in same room
            for p in world.players.players:
                if player.name == p.name:
                    continue
                if p.location_id == player.location_id:
                    await self.send_msg(f"You notice {player.name} look to the {avail_exit['direction'][1]}.", "info", p.websocket)

            player, world = await self.process_room(avail_exit["id"], player, world)
        else:
            for direction in MudDirections.pretty_directions:
                if (
                    wanted_direction.lower() == direction[0].lower()
                    or wanted_direction.lower() == direction[1].lower()
                ):
                    await self.send_msg(f"{direction[1]} is not a valid direction to look.","error", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 

    # doesn't return anything, just sends messages
    async def process_look(self, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        await self.send_msg("You look around the room.", "info", player.websocket)

        # send message to any players in same room that you left
        for p in world.players.players:
            if player.name == p.name:
                continue
            if p.location_id == player.location_id:
                await self.send_msg(f"You notice {player.name} looking around the room.","info",p.websocket)
        player, world = await self.process_room(
            player.location_id, player, world, player.websocket, self.logger
        )
        LogUtils.debug(f"{method_name}: exit", self.logger) 

    # returns player, world
    async def process_get(self, command, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        wanted_item = command.split(" ", 1)[1].lower()
        found_item = False
        room = world.rooms.rooms[player.location_id]
        if world.rooms.rooms[player.location_id].items != []:
            for item in room.items:
                if wanted_item == item.name.lower():
                    found_item = True
                    await self.send_msg(f"You pick up {item.name}.", "info", player.websocket)
                    
                    # remove from room
                    room.items.remove(item)

                    # alert the rest of the room
                    for room_player in room.players:
                        if room_player.websocket != player.websocket:
                            await self.send_msg(f"{player.name} picks up {item.name}.","info",player.websocket)

                    # add to our inventory
                    player.inventory.append(item)
                    break
        if found_item == False:
            await self.send_msg(f"You cannot find {wanted_item}.", "error", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player, world

    # doesn't return anything, just sends messages
    async def process_inventory(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        if player.inventory == [] and player.money == []:
            await self.send_msg("You have nothing in your inventory.", "info", player.websocket)
        else:
            msg = "You have the following items in your inventory:<br>"
            for item in player.inventory:
                if item.equiped == True:
                    msg += f"* {item.name} (Equiped)<br>"
                else:
                    msg += f"* {item.name}<br>"

            # get money
            money = len(player.money)
            if money > 0:
                msg += f"{money} copper<br>"
            else:
                msg += f"You have no money.<br>"
            await self.send_message(MudEvents.InventoryEvent(msg), player.websocket)

        LogUtils.debug(f"{method_name}: exit", self.logger) 

    # doesn't return anything, just sends messages
    async def process_search(self, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        rand = random()
        success = rand < (player.perception / 100)
        if success == True:
            if len(world.rooms.rooms[player.location_id].hidden_items) > 0:
                for item in world.rooms.rooms[player.location_id].hidden_items:
                    await self.send_message(MudEvents.InfoEvent(f"You found {item.name}!"), player.websocket)

                    # remove from "hidden items"
                    world.rooms.rooms[player.location_id].hidden_items.remove(item)

                    # add to items in room
                    world.rooms.rooms[player.location_id].items.append(item)
            else:
                await self.send_message(MudEvents.InfoEvent("After an exhaustive search, you find nothing and give up."), player.websocket)
        else:
            await self.send_message(MudEvents.InfoEvent("You search around but notice nothing."), player.websocket)

        LogUtils.debug(f"{method_name}: exit", self.logger) 

    # returns player, world
    async def process_drop(self, command, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        wanted_item = command.split(" ", 1)[1]
        player, world = await self.command_utility.drop_item(
            wanted_item, player, world
        )
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player, world

    async def process_hide_item(self, command, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        wanted_item = command.split(" ", 1)[1]
        found_item = False

        # check if it's in our inventory
        item_obj = None
        for item_in_inv in player.inventory:
            if wanted_item.lower() == item_in_inv.name.lower():
                item_obj = item_in_inv
                found_item = True
                break

        if found_item == True:
            # remove from inventory
            player.inventory.remove(item_obj)
            await self.send_message(MudEvents.InfoEvent(f"You hid {item_obj.name}."), player.websocket)
            world.rooms.rooms[player.location_id].hidden_items.append(item_obj)
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
        for item in player.inventory:
            if item.name.lower() == wanted_item.lower():
                await self.send_message(MudEvents.InfoEvent(f"You equip {item.name}."), player.websocket)
                item.equiped = True
                found_item = True
                found_item = item

        # if you eq'd an item, deselect any previous items
        for item in player.inventory:
            if (
                found_item.item_type == item.item_type and item.equiped == True
            ) and found_item.name != item.name:
                await self.send_message(f"You unequip {item.name}.", "info", player.websocket)
                item.equiped = False
        if found_item == None:
            await self.send_msg(f"You cannot equip {wanted_item}.", "error", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player

    async def process_system_command(self, command, extra, player, world):
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
            world = await self.world.players.unregister(world, player, True)
            player, world = await self.world.players.register(world, player)      
            await self.send_msg(f"{extra["name"]} is now known as {player.name}.", "changename", player.websocket, player.name)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player
    
    async def process_stat(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        msg = f"Hello {player.name}<br>"
        msg += "**************************************************<br>"
        msg += f"Level: {player.level}<br>"
        msg += f"Experience: {player.experience}<br>"
        msg += "**************************************************<br>"
        msg += "You have the following attributes:<br>"
        msg += f"* Health {player.hitpoints}<br>"
        msg += f"* Strength {player.strength}<br>"
        msg += f"* Agility {player.agility}<br>"
        msg += f"* Perception {player.perception}<br>"
        msg += "**************************************************"
        await self.send_msg(msg, "info", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player

    async def process_exp(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        await self.send_msg(f"You have {player.experience} experience.", "info", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player

    async def process_attack_mob(self, command, player, world):        
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

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
                for p in world.rooms.rooms[player.location_id].players:
                    if p.name == player.name:
                        await self.send_msg(f"You begin to attack {current_monster.name}!", "info", player.websocket)
                        p.in_combat = current_monster
                    else:
                        await self.send_msg(f"{player.name} begins to attack {current_monster.name}!", "info", p.websocket)

                # if you die and go to the crypt then your room id will change..
                while current_monster.hitpoints > 0 and player.location_id == world.rooms.rooms[player.location_id].id:
                    # determine attack damage
                    weapon = self.utility.get_equiped_weapon(player, self.logger)
                    attack_potential = weapon.damage_potential

                    # for number of swings here
                    num_swings = 1
                    num_swings += int(player.agility / weapon.weight_class.value)

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
                        damage += dice * damage_multipler * player.strength

                    for p in world.rooms.rooms[player.location_id].players:
                        response = ""
                        if player.name == p.name:
                            if damage == 0:
                                response = f"You swing wildly and miss!"
                            else:
                                if num_swings == 1:
                                    response = f"You {weapon.verb} {current_monster.name} with your {weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"You {weapon.verb} {current_monster.name} {num_swings} times with your {weapon.name.lower()} for {str(damage)} damage!"
                                await self.send_msg(response, "you_attack", player.websocket)
                        else:
                            if damage == 0:
                                response = f"{player.name} swings wildly and misses!"
                            else:
                                if num_swings == 1:
                                    response = f"{player.name} {weapon.plural_verb} {current_monster.name} with their {weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"{player.name} {weapon.plural_verb} {current_monster.name} {num_swings} times with their {weapon.name.lower()} for {str(damage)} damage!"
                                await self.send_msg(response,"you_attack",p.websocket)

                    # subtract from monsters health
                    current_monster.hitpoints = current_monster.hitpoints - damage

                    if current_monster.hitpoints <= 0:
                        # set monster as dead
                        await current_monster.kill(world.rooms.rooms[player.location_id], self.logger)

                        for p in world.rooms.rooms[player.location_id].players:
                            if p.in_combat == current_monster:
                                # give experience
                                p.experience += current_monster.experience

                                # send defeat message
                                msg = f"You vanquished {current_monster.name}!<br>You received {current_monster.experience} experience."
                                await self.send_msg(msg, "event", p.websocket)

                                # set combat back to none so we can fight someone else
                                p.in_combat = None

                                # show room
                                player, world = await self.process_room(player.location_id, player, world)

                        # add (Dead) to monster
                        current_monster.name = f"{current_monster.name} (Dead)"
                    else:
                        await asyncio.sleep(3)
            else:
                await self.send_msg(f"You cannot attack {current_monster.name}.  You are already in combat with {player.in_combat.name}.", "error", player.websocket)
        else:
            await self.send_msg(f"{wanted_monster} is not a valid attack target.","error", player.websocket)
        world.rooms.rooms[player.location_id].monsters = room_monsters
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player

    async def process_loot(self, command, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        wanted_monster = command.split(" ", 1)[1]  # loot skeleton

        # see if this monster is in the room.
        current_monster = None
        for monster in world.rooms.rooms[player.location_id].monsters:
            monster_name = monster.name.lower().strip()
            monster_name_parts = monster_name.split(" ")
            for name in monster_name_parts:
                if name.startswith(wanted_monster):
                    current_monster = monster
                    break

        if current_monster == None:
            await self.send_msg(f"You cannot loot {wanted_monster}", "info", player.websocket)
        else:
            if monster.is_alive == True:
                await self.send_msg(f"You cannot loot {current_monster.name}", "info", player.websocket)
            else:
                # take money
                monster_name = current_monster.name.replace("(Dead) ", "")
                if len(current_monster.money) > 0:
                    player.money.extend(current_monster.money)
                    msg = f"You take {len(current_monster.money)} copper from {monster_name}."
                    await self.send_msg(msg, "info", player.websocket)

                    # alert the rest of the room
                    for room_player in world.rooms.rooms[player.location_id].players:
                        if room_player.websocket != player.websocket:
                            await self.send_msg(f"{player.name} picks up {len(current_monster.money)} copper from {monster_name}.","info",player.websocket)

                    # remove from monster
                    current_monster.money = 0
                else:
                    await self.send_msg(f"You found no coins on {monster_name}.", "info", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player

    async def process_who(self, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        players = ""
        for player in world.players.players:
            players += f"{player.name}<br>"

        await self.send_msg(f"Players Online:<br>{players}", "info", player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player

    async def process_comms(self, command, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        if command.startswith("/say "):
            msg = command.split(" ", 1)[1]
            for p in world.players.players:
                if p.name == player.name:
                    await self.send_msg(f'You say "{msg}"', "info", p.websocket)
                else:
                    await self.send_msg(f'{player.name} says "{msg}"', "info",p.websocket)
        # elif command.startswith('/yell '): # can be heard from ajoining rooms
        #     pass
        # else: # it's a telepath
        #     pass
        LogUtils.debug(f"{method_name}: exit") 
        return player

    async def process_rest(self, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        monsters_in_room = len(world.rooms.rooms[player.location_id].monsters)
        if player.in_combat == True or monsters_in_room > 0:
            await self.send_msg("You cannot rest at this time. You are in combat.", "info", player.websocket)
        else:
            # check if in combat

            # if not...

            # simple message staying you're starting to rest
            await self.send_msg("You start to rest.", "info", player.websocket)

            # set an attribute that we can use later
            player.resting = True

        # press enter (refresh the room)
        player, world = await self.process_room(player.location_id, player)
        
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return room
    
    # main function that runs all the rest
    async def run_command(self, command, player, world, extra = ""):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)    
        LogUtils.debug(f'Command: "{command}"', self.logger)
        command = command.lower()

        # send back the command we received as info - (this could just be printed client side and save the traffic cost)
        await self.send_message(MudEvents.CommandEvent(command), player.websocket)

        # if the player is dead, don't do anything..
        if player.hitpoints <= 0:
            return player

        # process each command
        if command == "":
            player = await world.rooms.process_room(player.location_id, player, world)
        elif command == "help":  # display help
            player = await self.process_help(player)
        elif command in MudDirections.directions:  # process direction
            player = await self.process_direction(command, player, world)
        elif command == "l" or command == "look":  # look
            player = await self.process_look(player, world)
        elif command.startswith("l ") or command.startswith("look "):  # look <direction>
            player = await self.process_look_direction(command, player, world)
        elif command.startswith("g ") or command.startswith("get "):  # get
            player = await self.process_get(command, player, world)
        elif command == "i" or command == "inv" or command == "inventory":  # inv
            player = await self.process_inventory(player)
        elif command == "sea" or command == "search":  # search
            player = await self.process_search(player, world)
        elif command.startswith("dr ") or command.startswith("drop "):  # drop
            player = await self.process_drop(command, player)
        elif command.startswith("hide ") or command.startswith("stash "):  # hide
            player = await self.process_hide_item(command, player, world)
        elif command.startswith("eq ") or command.startswith("equip "):  # eq
            player = await self.process_equip_item(command, player)
        elif command.startswith("system "):  # a system command like changing username
            player = await self.process_system_command(command, extra, player, world)
        elif command == "stat":  # stat
            player = await self.process_stat(player)
        elif (command.startswith("a ")  or command.startswith("att ") or command.startswith("attack ")):  # attack
            asyncio.create_task(
                self.process_attack_mob(command, player, world)
            )
        elif command == ("exp") or command == ("experience"):  # experience
            player = await self.process_exp(player)
        elif command.startswith("loot "):  # loot corpse
            player = await self.process_loot(command, player, world)
        elif command == ("who"):
            player = await self.process_who(player, world)
        elif command.startswith("/"):
            player = await self.process_comms(command, player, world)
        elif command == "rest":
            player = await self.process_rest(player, world)
        else:  # you're going to say it to the room..
            await self.send_msg(f'"{command}" is not a valid command.', "info", player.websocket)

        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player
