from typing import List

from game.enums.defence_effects import DefenceEffects
from class_types.item_type import ItemType


class ItemTypeArmor(ItemType):
    defences = List[DefenceEffects]

    def __init__(self, name, item_type, weight, verb, plural_verb, description, quality, defences):
        super().__init__(name, item_type, weight, verb, plural_verb, description, quality)
        self.defences = defences
