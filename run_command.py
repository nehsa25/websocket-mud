from random import random, randint
from log_utils import LogUtils, Level
from items import Items

class Command:
    @staticmethod
    def check_inventory(item, player, logger=None):
        LogUtils.info(f"check_inventory Returning: {str(found_item)}", logger)
        return found_item


        # # if it's an "drop" command
        # elif command.startswith('d ') or command.startswith('drop '):
        #     wanted_item = command.split(' ', 1)[1] 
        #     found_item = False
        #     if Command.check_inventory(wanted_item, player) == True:
        #         found_item = True
        #         # remove from inventory
        #         player.inventory.remove(wanted_item)
        #         response = f"You dropped {wanted_item}"
        #         room['items'].append(wanted_item)
        #     if found_item == False:
        #         response = f"You can't drop {wanted_item}"



    @staticmethod
    def run_command(command, room, player, logger=None):
        # directions
        up = ('u', 'Up')
        down = ('d', 'Down')
        north = ('n', 'North')
        south = ('s', 'South')
        east = ('e', 'East')
        west = ('w', 'West')
        northwest = ('nw', 'Northwest')
        northeast = ('ne', 'Northeast')
        southeast = ('se', 'Southeast')
        southwest = ('sw', 'Southwest')
        directions = [up[0], up[1], down[0], down[1], north[0], north[1].lower(), south[0], south[1].lower(), east[0], east[1].lower(), west[0], west[1].lower(), northwest[0], northwest[1].lower(), northeast[0], northeast[1].lower(), southeast[0], southeast[1].lower(), southwest[0], southwest[1].lower()]
        pretty_directions = [up, down, north, south, east, west, northwest, northeast, southeast, southwest]
        LogUtils.debug(f"Command: \"{command}\"", logger)
        response = ""
        command = command.lower()
        if command == 'help':
            response = "look, get, dig, inventory, drop, search, hide, stash"
        
        # if it's a direction do this...        
        elif command.lower() in directions:
            found_exit = False
            for available_exit in room["exits"]:
                if command == available_exit["direction"]:    
                    for direction in pretty_directions:
                        if command.lower() == direction[0] or command.lower() == direction[1].lower():
                            response = f"You travel {direction[1]}."                            
                    player.location = available_exit["id"]
                    found_exit = True
                    break
            if found_exit == False:
                for direction in pretty_directions:
                    if command.lower() == direction[0] or command.lower() == direction[1].lower():
                        response = f"You cannot go {direction[1]}."

        # if it's a look
        elif command == "" or command == 'l' or command == 'look':
            response = f"{player.name} looks around the room."

        # if it's a "get" command        
        elif command.startswith('g ') or command.startswith('get '):
            wanted_item = command.split(' ', 1)[1].lower()
            found_item = False
            if room['items'] != []:
                for item in room['items']:
                    if wanted_item == item.name.lower():
                        found_item = True
                        response = f"You picked up {item.name}."
                        # remove from room
                        room['items'].remove(item)
                        # add to our inventory
                        player.inventory.append(item)
                        break
            if found_item == False:
                response = f"You cannot find {wanted_item}."

        # if it's an "inv" command
        elif command == 'i' or command == 'inv' or command == 'inventory':
            if player.inventory != []:
                response = "You have the following items in your inventory:<br>"
                for item in player.inventory:
                    response += "* " + item.name + "<br>"
            else:
                response = "You have nothing in your inventory."

        # if it's an "dig grave" command
        elif command == 'dig':
            # check if user has shovel
            if Items.shovel in player.inventory:
                if len(room['grave_items']) > 0:
                    response = f"You found something while digging!"
                    for item in room['grave_items']:
                        # remove item from hidden items
                        room['grave_items'].remove(item)
                        # add to items in room
                        room['items'].append(item)
            else:
                response = "You need a shovel to dig."

        # if it's an "search" command
        elif command == 'sea' or command == 'search':
            response = "You search around.."
            rand = random() 
            success = rand < (player.perception / 100)
            if success == True:
                if len(room['hidden_items']) > 0:
                    for item in room['hidden_items']:
                        response += "<br>You found something!"
                        # remove from "hidden items"
                        room['hidden_items'].remove(item)
                        # add to items in room
                        room['items'].append(item)
                else:
                    response += "<br>After an exhaustive search, you find nothing."
            else:
                response += f"<br>You notice nothing."

        # if it's an "drop" command
        elif command.startswith('d ') or command.startswith('drop '):
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
                response = f"You dropped {item_obj.name}"
                room['items'].append(item_obj)
            else:
                response = f"You can't drop {wanted_item}"

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
                response = f"You hid {item_obj.name}."
                room['hidden_items'].append(item_obj)
            else:
                response = f"You aren't carrying {wanted_item} to hide."

        # if it's an "equip" command
        elif command.startswith('eq ') or command.startswith('equip '):
            wanted_item = command.split(' ', 1)[1]

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
                    # see what weapon we have equiped.
                    equip = False
                    
                    # determine attack damage
                    attack_potential = "1d2"
                    if equip == True:
                        # set attack_potential to item damage_potential
                        pass

                    # attack monster
                    obj = attack_potential.split('d') # obj = obj[0] == 1, obj[1] == 2
                    dice = int(obj[0]) # 1
                    damage_potential = int(obj[1]) # 2
                    damage_multipler = randint(1, damage_potential)
                    damage = dice * damage_multipler
                    response = f"You punch {monster.name} for {str(damage)} damage!"

                    # subtract from monsters health
                    monster.hitpoints = monster.hitpoints - damage

                    if monster.hitpoints <= 0:
                        response = f"You vanquished {monster.name}!"
                        room_monsters.remove(monster)
            room['monsters'] = room_monsters

        else:
            response = "I don't understand that command."



        return player, response