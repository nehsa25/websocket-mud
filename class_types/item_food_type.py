from typing import List
from game.enums.effects_food import EffectsFood
from class_types.item_type import ItemType


class ItemFoodType(ItemType):
    effects: List[EffectsFood]

    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        quality,
        effects: List[EffectsFood],
    ):
        super().__init__(
            name, item_type, weight, verb, plural_verb, description, quality
        )
        self.effects = effects
