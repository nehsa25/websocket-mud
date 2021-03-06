import time
import asyncio
import json
from random import random, randint

# my stuff
from log_utils import LogUtils, Level
from muddirections import MudDirections
from utility import Utility
from command_utility import CommandUtility

class Command:
    @staticmethod
    async def process_room(new_room_id, player, world, websocket, logger):
        new_room = await world.get_room(new_room_id)

        # get the description
        description = new_room["description"]

        # show items
        items = ""
        if len(new_room['items']) > 0:
            for item in new_room['items']:
                items += item.name + ', '
            items = items[0:len(items)-2]

        # offer possible exits
        exits = ""
        for available_exit in new_room["exits"]:
            exits += available_exit['direction'][1] + ', '
        exits = exits[0:len(exits)-2]

        # show monsters
        monsters = ""
        for monster in new_room["monsters"]:
            monsters += monster.name + ', '
        monsters = monsters[0:len(monsters)-2]

         # show people
        people = ""
        for world_player in world.players:
            if player.name == world_player.name:
                continue
            if world_player.location == new_room_id:
                people += world_player.name + ', '
        if people != "":
            people = people[0:len(people)-2]

        # formulate message to client
        json_msg = {
            "type": 'room',
            "name": new_room["name"],
            "description": description,
            "items": items,
            "exits": exits,
            "monsters": monsters,
            "people": people
        }

        LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
        await websocket.send(json.dumps(json_msg))
        return player, world

    @staticmethod
    async def process_help(player, world, websocket, logger):
        help_msg = "look, get, inventory, drop, search, hide, stash, equip"
        await Utility.send_msg(help_msg, 'info', websocket, logger)
        return player, world

    @staticmethod
    async def process_direction(wanted_direction, player, world, websocket, logger):
        # stop resting                            
        if player.resting == True:
            player.resting = False
            await Utility.send_msg("You are no longer resting.", 'info', websocket, logger)
            
        room = await world.get_room(player.location)
        found_exit = False
        for avail_exit in room["exits"]:
            if wanted_direction == avail_exit["direction"][0].lower() or wanted_direction == avail_exit["direction"][1].lower():
                # send message to any players in same room that you left
                for world_player in world.players:
                    if player.name == world_player.name:
                        continue
                    if world_player.location == player.location:
                        await Utility.send_msg(f"{player.name} travels {avail_exit['direction'][1].lower()}.", 'info', world_player.websocket, logger)

                await Utility.send_msg(f"You travel {avail_exit['direction'][1].lower()}.", 'info', websocket, logger)   
                player.in_combat = None
                player, world = await world.move_room(avail_exit["id"], player, world, websocket, logger)

                # send message to any players in same room that you're here
                for world_player in world.players:
                    if player.name == world_player.name:
                        continue
                    if world_player.location == player.location:
                        opp_direction = None
                        for opp_dir in MudDirections.opp_directions:
                            if avail_exit['direction'] == opp_dir[0]:
                                 opp_direction = opp_dir[1]
                            if avail_exit['direction'] == opp_dir[1]:
                                opp_direction = opp_dir[0]

                        await Utility.send_msg(f"{player.name} arrives from the {opp_direction[1].lower()}.", 'info', world_player.websocket, logger)

                found_exit = True
                break
        if found_exit == False:
            for direction in MudDirections.pretty_directions:
                if wanted_direction.lower() == direction[0].lower() or wanted_direction.lower() == direction[1].lower():
                    await Utility.send_msg(f"You cannot go {direction[1]}.", 'error', websocket, logger)   
        return player, world

    @staticmethod
    async def process_look_direction(command, player, world, websocket, logger):
        room = await world.get_room(player.location)
        wanted_direction = command.split(' ', 1)[1].lower()
        valid_direction = False

        # check if it's a valid direction in the room
        for avail_exit in room["exits"]:
            if wanted_direction == avail_exit["direction"][0].lower() or wanted_direction == avail_exit["direction"][1].lower():
                valid_direction = True
                break

        if valid_direction == True:
            await Utility.send_msg(f"You look to the {avail_exit['direction'][1]}", 'info', websocket, logger)

            # send message to any players in same room
            for world_player in world.players:
                if player.name == world_player.name:
                    continue
                if world_player.location == player.location:
                   await Utility.send_msg(f"You notice {player.name} look to the {avail_exit['direction'][1]}.", 'info', world_player.websocket, logger)


            player, world = await Command.process_room(avail_exit["id"], player, world, websocket, logger)
        else: 
            for direction in MudDirections.pretty_directions:
                if wanted_direction.lower() == direction[0].lower() or wanted_direction.lower() == direction[1].lower():
                    await Utility.send_msg(f"{direction[1]} is not a valid direction to look.", 'error', websocket, logger)
            
        return player, world

    @staticmethod
    async def process_look(player, world, websocket, logger):
        await Utility.send_msg("You look around the room.", 'info', websocket, logger)

        # send message to any players in same room that you left
        for world_player in world.players:
            if player.name == world_player.name:
                continue
            if world_player.location == player.location:
                await Utility.send_msg(f"You notice {player.name} looking around the room.", 'info', world_player.websocket, logger)

        return await Command.process_room(player.location, player, world, websocket, logger)

    @staticmethod
    async def process_get(command, player, world, websocket, logger):
        room = await world.get_room(player.location)
        wanted_item = command.split(' ', 1)[1].lower()
        found_item = False
        if room['items'] != []:
            for item in room['items']:
                if wanted_item == item.name.lower():
                    found_item = True
                    await Utility.send_msg(f"You pick up {item.name}.", 'info', websocket, logger)
                    # remove from room
                    room['items'].remove(item)

                    # alert the rest of the room
                    for player in room['players']:
                        if websocket != player.websocket:
                            await Utility.send_msg(f"{player.name} picks up {item.name}.", 'info', player.websocket, logger)

                    # add to our inventory
                    player.inventory.append(item)
                    break
        if found_item == False:
            await Utility.send_msg(f"You cannot find {wanted_item}.", 'error', websocket, logger)
        return player, world

    @staticmethod
    async def process_inventory(player, world, websocket, logger):
        if player.inventory == [] and player.money == []:
            await Utility.send_msg("You have nothing in your inventory.", 'info', websocket, logger)
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

            await Utility.send_msg(msg, 'info', websocket, logger)
        return player, world

    @staticmethod
    async def process_search(player, world, websocket, logger):
        room = await world.get_room(player.location)
        rand = random() 
        success = rand < (player.perception / 100)
        if success == True:
            if len(room['hidden_items']) > 0:
                for item in room['hidden_items']:
                    await Utility.send_msg("You found something!", 'info', websocket, logger)

                    # remove from "hidden items"
                    room['hidden_items'].remove(item)

                    # add to items in room
                    room['items'].append(item)
            else:
                await Utility.send_msg("After an exhaustive search, you find nothing.", 'info', websocket, logger)
        else:
            await Utility.send_msg("You search around but notice nothing.", 'info', websocket, logger)
        return player, world

    @staticmethod
    async def process_drop(command, player, world, websocket, logger):
        wanted_item = command.split(' ', 1)[1]         
        found_item = await CommandUtility.drop_item(wanted_item, player, world, websocket, logger) 
        found_coin = await CommandUtility.drop_coin(wanted_item, player, world, websocket, logger)

        # if we didn't find the item, check if it's currency
        if not found_item and not found_coin:
            await Utility.send_msg(f"You can't drop {wanted_item}", 'error', websocket, logger)
            
        return player, world

    @staticmethod
    async def process_hide_item(command, player, world, websocket, logger):
        room = await world.get_room(player.location)
        wanted_item = command.split(' ', 1)[1] 
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
            await Utility.send_msg(f"You hid {item_obj.name}.", 'info', websocket, logger)
            room['hidden_items'].append(item_obj)
        else:
            await Utility.send_msg(f"You aren't carrying {wanted_item} to hide.", 'error', websocket, logger)
        return player, world

    @staticmethod
    async def process_equip_item(command, player, world, websocket, logger):
        wanted_item = command.split(' ', 1)[1]
        found_item = None

        # check if the item is in our inventory
        for item in player.inventory:
            if item.name.lower() == wanted_item.lower():
                await Utility.send_msg(f"You equip {item.name}.", 'info', websocket, logger)
                item.equiped = True
                found_item = True
                found_item = item

        # if you eq'd an item, deselect any previous items
        for item in player.inventory:
            if (found_item.item_type == item.item_type and item.equiped == True) and found_item.name != item.name:
                await Utility.send_msg(f"You unequip {item.name}.", 'info', websocket, logger)
                item.equiped = False
        if found_item == None:
            await Utility.send_msg(f"You cannot equip {wanted_item}.", 'error', websocket, logger)
        return player, world

    @staticmethod
    async def process_stat(player, world, websocket, logger):
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
        await Utility.send_msg(msg, 'info', websocket, logger)
        return player, world

    @staticmethod
    async def process_exp(player, world, websocket, logger):
        await Utility.send_msg(f"You have {player.experience} experience.", 'info', websocket, logger)
        return player, world

    @staticmethod
    async def process_attack_mob(command, player, world, websocket, logger):
        # get our room
        room = await world.get_room(player.location)

        # att skeleton
        wanted_monster = command.split(' ', 1)[1].lower() # wanted_monster == skeleton

        # see if this monster is in the room.
        current_monster = None
        room_monsters = room['monsters']
        for monster in room_monsters: 
            monster_name = monster.name.lower().strip()
            monster_name_parts = monster_name.split(' ')
            for name in monster_name_parts:
                if name.startswith(wanted_monster) and monster.is_alive == True:
                    current_monster = monster
                    break

        if current_monster != None:
            if player.in_combat == None:
                for world_player in room['players']:
                    if world_player.name == player.name: 
                        await Utility.send_msg(f"You begin to attack {current_monster.name}!", 'info', websocket, logger)
                        world_player.in_combat = current_monster
                    else:
                        await Utility.send_msg(f"{player.name} begins to attack {current_monster.name}!", 'info', world_player.websocket, logger)
                        
                # if you die and go to the crypt then your room id will change..
                while current_monster.hitpoints > 0 and player.location == room['id']:
                    # update our room
                    room = await world.get_room(player.location)

                    # determine attack damage
                    weapon = CommandUtility.get_equiped_weapon(player, logger)
                    attack_potential = weapon.damage_potential  

                    # for number of swings here 
                    num_swings = 1
                    num_swings += int(player.agility / weapon.weight_class.value)
                    
                    LogUtils.debug(f"We're going to swing {num_swings} times!", logger)

                    damage = 0
                    for x in range(0, num_swings):
                        LogUtils.debug(f"Swinging!", logger)
                        # attack monster
                        obj = attack_potential.split('d') # obj = obj[0] == 1, obj[1] == 2
                        dice = int(obj[0]) # 1
                        damage_potential = int(obj[1]) # 2
                        damage_multipler = randint(0, damage_potential)
                        damage += dice * damage_multipler * player.strength
                    
                    for world_player in room['players']:
                        response = ""
                        if player.name == world_player.name: 
                            if damage == 0:
                                response = f"You swing wildly and miss!"
                            else:
                                if num_swings == 1:
                                    response = f"You {weapon.verb} {current_monster.name} with your {weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"You {weapon.verb} {current_monster.name} {num_swings} times with your {weapon.name.lower()} for {str(damage)} damage!"
                                await Utility.send_msg(response, 'you_attack', websocket, logger)
                        else:
                            if damage == 0:
                                response = f"{player.name} swings wildly and misses!"
                            else:
                                if num_swings == 1:
                                    response = f"{player.name} {weapon.plural_verb} {current_monster.name} with their {weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"{player.name} {weapon.plural_verb} {current_monster.name} {num_swings} times with their {weapon.name.lower()} for {str(damage)} damage!"
                                await Utility.send_msg(response, 'you_attack', world_player.websocket, logger)
                

                    # subtract from monsters health
                    current_monster.hitpoints = current_monster.hitpoints - damage

                    if current_monster.hitpoints <= 0:
                        # set monster as dead
                        await current_monster.kill(room, logger)

                        for world_player in room['players']:
                            if world_player.in_combat == current_monster:
                                # give experience
                                world_player.experience += current_monster.experience

                                # send defeat message
                                msg = f"You vanquished {current_monster.name}!<br>You received {current_monster.experience} experience."
                                await Utility.send_msg(msg, 'event', world_player.websocket, logger)
                                
                                # set combat back to none so we can fight someone else
                                world_player.in_combat = None

                                # show room
                                await Command.process_room(player.location, player, world, world_player.websocket, logger)
                        
                        # add (Dead) to monster 
                        current_monster.name = f"{current_monster.name} (Dead)"
                    else:
                        await asyncio.sleep(3)
            else:
                await Utility.send_msg(f"You cannot attack {current_monster.name}.  You are already in combat with {player.in_combat.name}.", 'error', websocket, logger)
        else:
            await Utility.send_msg(f"{wanted_monster} is not a valid attack target.", 'error', websocket, logger)
        room['monsters'] = room_monsters
        return player, world

    @staticmethod
    async def process_loot(command, player, world, websocket, logger):
        room = await world.get_room(player.location)
        wanted_monster = command.split(' ', 1)[1] # loot skeleton

        # see if this monster is in the room.
        current_monster = None
        for monster in room['monsters']:
            monster_name = monster.name.lower().strip()
            monster_name_parts = monster_name.split(' ')
            for name in monster_name_parts:
                if name.startswith(wanted_monster):
                    current_monster = monster
                    break

        if current_monster == None:
            await Utility.send_msg(f"You cannot loot {wanted_monster}", 'info', websocket, logger)
        else:
            if monster.is_alive == True:
                await Utility.send_msg(f"You cannot loot {current_monster.name}", 'info', websocket, logger)
            else:
                # take money
                monster_name = current_monster.name.replace('(Dead) ', '')
                if len(current_monster.money) > 0:
                    player.money.extend(current_monster.money)
                    msg = f"You take {len(current_monster.money)} copper from {monster_name}."
                    await Utility.send_msg(msg, 'info', websocket, logger)

                    # alert the rest of the room
                    for player in room['players']:
                        if websocket != player.websocket:
                            await Utility.send_msg(f"{player.name} picks up {len(current_monster.money)} copper from {monster_name}.", 'info', player.websocket, logger)

                    # remove from monster
                    current_monster.money = 0
                else:
                    await Utility.send_msg(f"You found no coins on {monster_name}.", 'info', websocket, logger)
        return player, world

    @staticmethod
    async def process_who(player, world, websocket, logger):
        players = ""
        for player in world.players:
            players += f"{player.name}<br>"

        await Utility.send_msg(f"Players Online:<br>{players}", 'info', websocket, logger)
        return player, world 

    @staticmethod
    async def process_comms(command, player, world, websocket, logger):
        if command.startswith('/say '):
            msg = command.split(' ', 1)[1]
            for world_player in world.players:
                if world_player.name == player.name:
                    await Utility.send_msg(f"You say \"{msg}\"", 'info', world_player.websocket, logger)
                else:
                    await Utility.send_msg(f"{player.name} says \"{msg}\"", 'info', world_player.websocket, logger)
        # elif command.startswith('/yell '): # can be heard from ajoining rooms
        #     pass
        # else: # it's a telepath
        #     pass
        return player, world 

    @staticmethod
    async def process_rest(player, world, websocket, logger):
        room = await world.get_room(player.location)
        monsters_in_room = len(room['monsters'])
        if player.in_combat == True or monsters_in_room > 0:
            await Utility.send_msg("You cannot rest at this time.  You are in combat.", 'info', websocket, logger)
        else:
            # check if in combat

            # if not...

            # simple message staying you're starting to rest
            await Utility.send_msg("You start to rest.", 'info', websocket, logger)

            # set an attribute that we can use later
            player.resting = True

        # press enter (refresh the room)
        return await Command.process_room(player.location, player, world, websocket, logger)

    # main function that runs all the rest
    @staticmethod
    async def run_command(command, player, world, websocket, logger):
        LogUtils.debug(f"Command: \"{command}\"", logger)
        response = ""
        command = command.lower()

        # send back the command we received as info
        await Utility.send_msg(command, 'command', websocket, logger)

        # if the player is dead, don't do anything..
        if player.hitpoints <= 0:
            return player, world

        # process each command
        if command == "":
            player, world= await Command.process_room(player.location, player, world, websocket, logger)
        elif command == 'help': # display help
            player, world = await Command.process_help(player, world, websocket, logger)
        elif command in MudDirections.directions: # process direction
            player, world = await Command.process_direction(command, player, world, websocket, logger)
        elif command == 'l' or command == 'look': # look
            player, world = await Command.process_look(player, world, websocket, logger)
        elif command.startswith('l ') or command.startswith('look '): # look <direction>
            player, world = await Command.process_look_direction(command, player, world, websocket, logger)
        elif command.startswith('g ') or command.startswith('get '): # get
            player, world = await Command.process_get(command, player, world, websocket, logger)
        elif command == 'i' or command == 'inv' or command == 'inventory': # inv
            player, world = await Command.process_inventory(player, world, websocket, logger)
        elif command == 'sea' or command == 'search': # search
            player, world = await Command.process_search(player, world, websocket, logger)
        elif command.startswith('dr ') or command.startswith('drop '): # drop
            player, world = await Command.process_drop(command, player, world, websocket, logger)
        elif command.startswith('hide ') or command.startswith('stash '): # hide
            player, world = await Command.process_hide_item(command, player, world, websocket, logger)
        elif command.startswith('eq ') or command.startswith('equip '): # eq
            player, world = await Command.process_equip_item(command, player, world, websocket, logger)
        elif command == 'stat': # stat
            player, world = await Command.process_stat(player, world, websocket, logger)
        elif command.startswith('a ') or command.startswith('att ') or command.startswith('attack '): # attack
            asyncio.create_task(Command.process_attack_mob(command, player, world, websocket, logger))
        elif command == ('exp') or command == ('experience'): # experience
            player, world = await Command.process_exp(player, world, websocket, logger)
        elif command.startswith('loot '): # loot corpse
            player, world = await Command.process_loot(command, player, world, websocket, logger)
        elif command == ('who'):
            player, world = await Command.process_who(player, world, websocket, logger)
        elif command.startswith('/'):
            player, world = await Command.process_comms(command, player, world, websocket, logger)
        elif command == 'rest':
            player, world = await Command.process_rest(player, world, websocket, logger)
        else: # you're going to say it to the room..
            await Utility.send_msg(f"\"{command}\" is not a valid command.", 'info', websocket, logger)

        return player, world