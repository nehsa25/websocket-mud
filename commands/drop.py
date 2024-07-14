import inspect
from log_utils import LogUtils
from utility import Utility

class Drop(Utility):
    class DropUtility:
        logger = None

        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug(f"Initializing DropUtility() class", self.logger)

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
    
    logger = None
    description = "Drop an item from your inventory to the room floor."
    command = "drop[dr,d] <target>"
    examples = []
    drop_utility = None
    type = Utility.Share.Commands.DROP
    
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Drop() class", self.logger)
        self.drop_utility = Drop.DropUtility(logger)
        
    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        wanted_item = command.split(" ", 1)[1]
        player, world_state = await self.drop_utility.drop_item(
            wanted_item, player, world_state
        )
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world_state
