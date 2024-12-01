from enum import Enum
import inspect

from log_utils import LogUtils
from utility import Utility


class Item(Utility):
    name = None
    damage_potential = None
    weight_class = None
    item_type = None
    verb = None
    plural_verb = None
    equipped = False
    can_be_equipped = False
    description = None
    contents = None

    # item types
    class ItemType(Enum):
        WEAPON = 1
        ITEM = 2
        ARMOR_HEAD = 3
        ARMOR_FEET = 4
        ARMOR_HANDS = 5
        ARMOR_LEGS = 6
        ARMOR_TORSO = 7

    # weight classes
    class WeightClass(Enum):
        SUPER_LIGHT_WEIGHT = 3
        LIGHT_WEIGHT = 4
        MEDIUM_WEIGHT = 8
        HEAVY_WEIGHT = 10
        SUPER_HEAVY_WEIGHT = 15

    def __init__(
        self,
        name,
        item_type,
        damage_potential,
        weight_class,
        verb,
        plural_verb,
        description,
        contents=None,
    ):
        self.name = name
        self.damage_potential = damage_potential
        self.weight_class = weight_class
        self.item_type = item_type
        self.verb = verb
        self.plural_verb = plural_verb
        self.description = description
        self.contents = contents

    async def equip(self, player, action_eq=True):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if not self.can_be_equipped and action_eq == True:
            await self.world.self.world.utility.send_msg(
                f"You cannot wield {self.name}.", "info", player.websocket, self.logger
            ) 
            return
            
        if  action_eq == True and self.equipped == False:   
            self.equipped = True                        
            await self.world.self.world.utility.send_msg(
                f"You wield {self.name}.", "info", player.websocket, self.logger
            )
            await player.room.alert(f"You notice {player.name} equip {self.name}.", exclude_player=True, player=player)
            
        if  action_eq == False and self.equipped == True:   
            self.equipped = False                        
            await self.world.self.world.utility.send_msg(
                f"You unequip {self.name}.", "info", player.websocket, self.logger
            )
            await player.room.alert(f"You notice {player.name} unequip {self.name}.", exclude_player=True, player=player)
            
        LogUtils.debug(f"{method_name}: exit", self.logger)