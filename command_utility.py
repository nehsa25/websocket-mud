from utility import Utility
from items import Items
from item import Item

class CommandUtility:
    @staticmethod
    def get_equiped_weapon(player, logger):
        eq_item = Items.punch
        for item in player.inventory:
            if item.item_type == Item.ItemType.WEAPON and item.equiped == True:
                eq_item = item

        return eq_item

    @staticmethod
    async def drop_item(wanted_item, player, world, websocket, logger):
        room = await world.get_room(player.location)
        found_item = False

        # check if it's in our inventory
        item_obj = None
        for item_in_inv in player.inventory:
            if wanted_item.lower() == item_in_inv.name.lower():
                item_obj = item_in_inv
                found_item = True
                break

        if found_item == True:      
            # set eq'd to False
            item_obj.equiped = False

            # remove from inventory
            player.inventory.remove(item_obj)
            await Utility.send_msg(f"You dropped {item_obj.name}.", 'info', websocket, logger)
            room['items'].append(item_obj)
        return found_item

    @staticmethod
    async def drop_coin(wanted_item, player, world, websocket, logger):
        room = await world.get_room(player.location)
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
            room['items'].append(item_obj)

            # remove from player inventory
            player.inventory.remove(item_obj)
            await Utility.send_msg(f"You dropped {coin.Name}.", 'info', websocket, logger)
        return found_coin
