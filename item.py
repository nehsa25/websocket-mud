from enum import Enum


class Item:
    name = None
    damage_potential = None
    weight_class = None
    item_type = None
    verb = None
    plural_verb = None
    equiped = False
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
