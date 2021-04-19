import time
import asyncio
import json
from random import random, randint

# my stuff
from log_utils import LogUtils, Level
from items import Items
from item import Item
from muddirections import MudDirections

class Command:

    @staticmethod
    def get_equiped_weapon(player, logger=None):
        eq_item = Items.punch
        for item in player.inventory:
            if item.item_type == Item.ItemType.WEAPON and item.equiped == True:
                eq_item = item

        return eq_item


    @staticmethod
    async def run_command(command, room, player, websocket, logger=None):
        LogUtils.debug(f"Command: \"{command}\"", logger)
        response = ""
        command = command.lower()

        # if the player is dead, don't do anything..
        if player.hitpoints <= 0:
            return player

        # display usage information
        if command == 'help':
            response = "look, get, dig, inventory, drop, search, hide, stash"
        
        # if it's a direction do this...        
        elif command.lower() in MudDirections.directions:
            found_exit = False
            for avail_exit in room["exits"]:
                if command in avail_exit["direction"]:
                    json_msg = { "type": 'info', "info": f"You travel {avail_exit['direction'][1]}." }
                    LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                    await websocket.send(json.dumps(json_msg))               
                    player.location = avail_exit["id"]
                    found_exit = True
                    break
            if found_exit == False:
                for direction in MudDirections.pretty_directions:
                    if command.lower() in direction:
                        json_msg = { "type": 'info', "info": f"You cannot go {direction[1]}."}
                        LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                        await websocket.send(json.dumps(json_msg))

        # if it's a look
        elif command == "" or command == 'l' or command == 'look':
            json_msg = { "type": 'info', "info": f"{player.name} looks around the room."}
            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
            await websocket.send(json.dumps(json_msg))

        # if it's a "get" command        
        elif command.startswith('g ') or command.startswith('get '):
            wanted_item = command.split(' ', 1)[1].lower()
            found_item = False
            if room['items'] != []:
                for item in room['items']:
                    if wanted_item == item.name.lower():
                        found_item = True
                        json_msg = { "type": 'info', "info": f"You picked up {item.name}."}
                        LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                        await websocket.send(json.dumps(json_msg))
                        # remove from room
                        room['items'].remove(item)
                        # add to our inventory
                        player.inventory.append(item)
                        break
            if found_item == False:
                json_msg = { "type": 'info', "info": f"You cannot find {wanted_item}."}
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

        # if it's an "inv" command
        elif command == 'i' or command == 'inv' or command == 'inventory':
            if player.inventory != []:
                msg = "You have the following items in your inventory:<br>"
                for item in player.inventory:
                    if item.equiped == True:
                        msg += f"* {item.name} (Equiped)<br>"
                    else:
                        msg += f"* {item.name}<br>"

                json_msg = { "type": 'info', "info": msg}
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))
            else:
                json_msg = { "type": 'info', "info": "You have nothing in your inventory."}
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

        # if it's an "dig grave" command
        elif command == 'dig':
            # check if user has shovel
            if Items.shovel in player.inventory:
                if len(room['grave_items']) > 0:
                    json_msg = { "type": 'info', "info": f"You found something while digging!"}
                    LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                    await websocket.send(json.dumps(json_msg))
                    for item in room['grave_items']:
                        # remove item from hidden items
                        room['grave_items'].remove(item)
                        # add to items in room
                        room['items'].append(item)
            else:
                json_msg = { "type": 'info', "info": "You need a shovel to dig." }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

        # if it's an "search" command
        elif command == 'sea' or command == 'search':
            response = "You search around.."
            rand = random() 
            success = rand < (player.perception / 100)
            if success == True:
                if len(room['hidden_items']) > 0:
                    for item in room['hidden_items']:
                        json_msg = { "type": 'info', "info": "<br>You found something!" }
                        LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                        await websocket.send(json.dumps(json_msg))

                        # remove from "hidden items"
                        room['hidden_items'].remove(item)

                        # add to items in room
                        room['items'].append(item)
                else:
                    json_msg = { "type": 'info', "info": "<br>After an exhaustive search, you find nothing." }
                    LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                    await websocket.send(json.dumps(json_msg))
            else:
                json_msg = { "type": 'info', "info": f"<br>You notice nothing." }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

        # if it's an "drop" command
        elif command.startswith('dr ') or command.startswith('drop '):
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
                json_msg = { "type": 'info', "info": f"You dropped {item_obj.name}" }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))
                room['items'].append(item_obj)
            else:
                json_msg = { "type": 'info', "info": f"You can't drop {wanted_item}" }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

        # if it's an "hide" command
        elif command.startswith('hide ') or command.startswith('stash '):
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
                json_msg = { "type": 'info', "info": f"You hid {item_obj.name}." }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))
                room['hidden_items'].append(item_obj)
            else:
                json_msg = { "type": 'info', "info": f"You aren't carrying {wanted_item} to hide." }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

        # if it's an "equip" command
        elif command.startswith('eq ') or command.startswith('equip '):
            wanted_item = command.split(' ', 1)[1]
            found_item = False

            # check if the item is in our inventory
            for item in player.inventory:
                if item.name.lower() == wanted_item.lower():
                    json_msg = { "type": 'info', "info": f"You equip {item.name}." }
                    LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                    await websocket.send(json.dumps(json_msg))
                    item.equiped = True
                    found_item = True
            if found_item == False:
                json_msg = { "type": 'info', "info": f"You cannot equip {wanted_item}." }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

        # if it's a stat command
        elif command == 'stat':
            msg = "You have the following attributes:<br>"
            msg += f"* Health {player.hitpoints}<br>"
            msg += f"* Strength {player.strength}<br>"
            msg += f"* Perception {player.perception}"
            json_msg = { "type": 'info', "info": msg }
            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
            await websocket.send(json.dumps(json_msg))

        # if it's an "drink quaff" command
        elif command.startswith('drink ') or command.startswith('quaff '):
            wanted_drink = command.split(' ', 1)[1]

        # if it's an "Attack" command
        elif command.startswith('a ') or command.startswith('att ') or command.startswith('attack '):
            # att skeleton
            wanted_monster = command.split(' ', 1)[1] # wanted_monster == skeleton

            # see if this monster is in the room.
            room_monsters = room['monsters']
            for monster in room['monsters']:
                if wanted_monster.lower() == monster.name.lower():
                    json_msg = { "type": 'info', "info": f"You begin to attack {monster.name}!<br>" }
                    LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                    await websocket.send(json.dumps(json_msg))

                    # if you die and go to the crypt then your room ide will change..
                    while monster.hitpoints > 0 and player.location == room['id']:
                        # determine attack damage
                        weapon = Command.get_equiped_weapon(player, logger)
                        attack_potential = weapon.damage_potential  

                        # for number of swings here 
                        num_swings = 1
                        num_swings += int(player.dexerity / weapon.weight_class.value)
                        
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

                        if damage == 0:
                            response = f"You swing wildly and miss!<br>"
                        else:
                            response = f"{weapon.hit_message} {monster.name} {num_swings} times with your {weapon.name.lower()} for {str(damage)} damage!<br>"
                        json_msg = { "type": 'attack', "attack": response }
                        LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                        await websocket.send(json.dumps(json_msg))

                        # subtract from monsters health
                        monster.hitpoints = monster.hitpoints - damage

                        if monster.hitpoints <= 0:
                            json_msg = { "type": 'info', "info": f"You vanquished {monster.name}!" }
                            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                            await websocket.send(json.dumps(json_msg))
                            room_monsters.remove(monster)

                        await asyncio.sleep(3)
            room['monsters'] = room_monsters

        else:
            json_msg = { "type": 'error', "error": "I don't understand that command." }
            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
            await websocket.send(json.dumps(json_msg))

        return player