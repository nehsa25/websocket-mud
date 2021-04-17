from enum import Enum

class Item:
    name = None
    damage_potential = None
    weight_class = None

    # weight classes
    class WeightClass(Enum):
        SUPER_LIGHT_WEIGHT = 3
        LIGHT_WEIGHT = 4
        MEDIUM_WEIGHT = 8
        HEAVY_WEIGHT = 10
        SUPER_HEAVY_WEIGHT = 15

    def __init__(self, name, damage_potential, weight_class):
        self.name = name
        self.damage_potential = damage_potential
        self.weight_class = weight_class
    