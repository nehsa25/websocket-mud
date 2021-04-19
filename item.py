from enum import Enum

class Item:
    name = None
    damage_potential = None
    weight_class = None
    item_type = None
    hit_message = None
    equiped = False

    # item types
    class ItemType(Enum):
        ARMOR = 1
        WEAPON = 2
        ITEM = 3

    # weight classes
    class WeightClass(Enum):
        SUPER_LIGHT_WEIGHT = 3
        LIGHT_WEIGHT = 4
        MEDIUM_WEIGHT = 8
        HEAVY_WEIGHT = 10
        SUPER_HEAVY_WEIGHT = 15

    def __init__(self, name, item_type, damage_potential, weight_class, hit_message):
        self.name = name
        self.damage_potential = damage_potential
        self.weight_class = weight_class
        self.item_type = item_type
        self.hit_message = hit_message
    