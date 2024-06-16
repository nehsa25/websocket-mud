import inspect
from items import Items
from item import Item
from log_utils import LogUtils


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
            player.inventory.remove(item_obj)
            await self.send_msg(
                f"You dropped {coin.Name}.", "info", websocket, self.logger
            )
        else:
            await self.send_msg(f"You can't drop {wanted_item}", "error", player.websocket)
            
        return player, world
