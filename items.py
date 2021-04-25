from item import Item

class Items:
    stick = Item('Stick', Item.ItemType.WEAPON, '1d3', Item.WeightClass.LIGHT_WEIGHT, 'swish')
    shovel = Item('Shovel', Item.ItemType.WEAPON,'1d2', Item.WeightClass.MEDIUM_WEIGHT, 'thunk')
    helmet = Item('Helmet', Item.ItemType.ARMOR_HEAD, None, None, None)
    ring = Item('Ring', Item.ItemType.ITEM, None, None, None)
    cloth_pants = Item('Cloth Pants', Item.ItemType.ARMOR_LEGS, None, None, None)
    shirt = Item('Shirt', Item.ItemType.ARMOR_TORSO, None, None, None)
    lockpick = Item('Lockpick', Item.ItemType.ITEM, None, None, None)
    club = Item('Club', Item.ItemType.WEAPON, '1d4', Item.WeightClass.MEDIUM_WEIGHT, 'bludgeon')
    maul = Item('Maul', Item.ItemType.WEAPON, '1d5', Item.WeightClass.HEAVY_WEIGHT, 'smash')
    punch = Item('Punch', Item.ItemType.WEAPON, '1d2', Item.WeightClass.SUPER_LIGHT_WEIGHT, 'punch')
    dragon_tooth = Item('Dragon Tooth', Item.ItemType.WEAPON, '1d6', Item.WeightClass.SUPER_HEAVY_WEIGHT, 'poke')
