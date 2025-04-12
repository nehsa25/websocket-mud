import inspect
from item import Item
from log_utils import LogUtils
from money import Money
from mudevent import MudEvents
from utility import Utility


class Inventory(Utility):
    items = []
    money = None

    def __init__(self, items=[], money=Money(), logger=None):
        self.logger = logger
        LogUtils.debug("Initializing Inventory() class", self.logger)
        self.items = items
        self.money = money

    async def get_item(self, wanted_item, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        found = False
        for item in player.room.items:
            if wanted_item != item.name.lower():
                continue

            found = True

            # send message to player
            await player.send_message(MudEvents.InfoEvent(f"You pick up {item.name}."), player.websocket)

            # send message to room
            await player.room.alert(f"{player.name} picks up {wanted_item}.", exclude_player=True, player=player, event_type=MudEvents.InfoEvent)

            # add item to inventory
            self.items.append(item)
            await player.send_inventory()
            break

        if not found:
            await player.room.alert(f"{wanted_item} not found.", exclude_player=True, player=player, event_type=MudEvents.ErrorEvent)

        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def drop_item(self, wanted_item, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        found = False
        for item in player.room.items:
            if wanted_item != item.name.lower():
                continue

            found = True

            # send message to player
            await player.send_message(MudEvents.InfoEvent(f"You drop up {item.name}."), player.websocket)

            # send message to room
            await player.room.alert(f"{player.name} drops {wanted_item} to the ground.", exclude_player=True, player=player, event_type=MudEvents.ErrorEvent)

            
            
            # add item to inventory
            self.items.remove(item)
            await player.send_inventory()
            break

        if not found:
            await player.room.alert(f"You do not have {wanted_item}.", exclude_player=True, player=player, event_type=MudEvents.ErrorEvent)


        LogUtils.debug(f"{method_name}: exit", self.logger)

