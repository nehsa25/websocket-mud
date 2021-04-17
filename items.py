from item import Item

class Items:
    stick = Item('Stick', '1d3', Item.WeightClass.LIGHT_WEIGHT)
    shovel = Item('Shovel', '1d2', Item.WeightClass.MEDIUM_WEIGHT)
    helmet = Item('Helmet', None, None)
    ring = Item('Ring', None, None)
    cloth_pants = Item('Cloth Pants', None, None)
    shirt = Item('Shirt', None, None)
    lockpick = Item('Lockpick', None, None)
    club = Item('Club', '1d4', Item.WeightClass.HEAVY_WEIGHT)
    punch = Item('Punch', '1d2', Item.WeightClass.SUPER_LIGHT_WEIGHT)
    dragon_tooth = Item('Dragon Tooth', '1d4', Item.WeightClass.SUPER_HEAVY_WEIGHT)
