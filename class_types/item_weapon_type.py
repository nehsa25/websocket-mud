from typing import List

from game.enums.attack_effects import AttackEffects
from class_types.item_type import ItemType


class ItemWeaponType(ItemType):
    attacks = List[AttackEffects]
    damage = str  # this is a 1d6 type string

    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        quality,
        attacks,
        damage,
    ):
        super().__init__(
            name,
            item_type,
            damage,
            weight,
            verb,
            plural_verb,
            description,
            quality,
        )
        self.attacks = attacks
        self.damage = damage
