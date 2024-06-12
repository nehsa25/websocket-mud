from item import Item


class Items:
    stick = Item(
        "Stick",
        Item.ItemType.WEAPON,
        "1d3",
        Item.WeightClass.LIGHT_WEIGHT,
        "swish",
        "swishes",
        "A stick from a tree.",
    )
    shovel = Item(
        "Shovel",
        Item.ItemType.WEAPON,
        "1d2",
        Item.WeightClass.MEDIUM_WEIGHT,
        "thwack",
        "thwacks",
        "A shovel for digging holes.",
    )
    helmet = Item(
        "Helmet",
        Item.ItemType.ARMOR_HEAD,
        None,
        None,
        None,
        None,
        "A helmet to protect your head.",
    )
    ring = Item(
        "Ring", Item.ItemType.ITEM, None, None, None, None, "A ring that glows."
    )
    cloth_pants = Item(
        "Cloth Pants",
        Item.ItemType.ARMOR_LEGS,
        None,
        None,
        None,
        None,
        "Pants made of cloth.",
    )
    shirt = Item(
        "Shirt",
        Item.ItemType.ARMOR_TORSO,
        None,
        None,
        None,
        None,
        "A shirt made of cloth.",
    )
    lockpick = Item(
        "Lockpick",
        Item.ItemType.ITEM,
        None,
        None,
        None,
        None,
        "A lockpick for picking locks.",
    )
    club = Item(
        "Club",
        Item.ItemType.WEAPON,
        "1d4",
        Item.WeightClass.MEDIUM_WEIGHT,
        "bludgeon",
        "bludgeons",
        "A club for hitting things.",
    )
    maul = Item(
        "Maul",
        Item.ItemType.WEAPON,
        "1d5",
        Item.WeightClass.HEAVY_WEIGHT,
        "smash",
        "smashes",
        "A maul for smashing things.",
    )
    punch = Item(
        "Fists",
        Item.ItemType.WEAPON,
        "1d2",
        Item.WeightClass.SUPER_LIGHT_WEIGHT,
        "punch",
        "punches",
        "Your knuckles.  Scarred and bruised.  Partially healed scapes cris-cross your hands.",
    )
    dragon_tooth = Item(
        "Dragon Tooth",
        Item.ItemType.WEAPON,
        "1d6",
        Item.WeightClass.SUPER_HEAVY_WEIGHT,
        "poke",
        "pokes",
        "A tooth from a dragon.",
    )
    book = Item(
        "Dusty Book",
        Item.ItemType.ITEM,
        None,
        None,
        None,
        None,
        "A dusty book with a leather cover.",
        "Strange symbols are written on the pages.",
    )

    # "sword", "shield", "potion",
    # "gold", "key", "map", "compass",
    # "torch", "rope", "rations", "armor",
    # "helmet", "boots", "gloves",
    # "cloak", "ring", "amulet", "wand", "staff",
    # "scroll", "book", "gem", "jewel",
    # "coin", "bag", "backpack", "sack",
    # "pouch", "chest", "box",
    # "barrel", "cask", "bottle", "flask", "vial",
    # "jar", "jug", "pot", "pan", "plate", "bowl", "cup", "mug",
    # "glass", "pitcher", "lamp", "candle", "torch", "lantern",
    # "oil", "flint", "steel", "tinder", "rope", "chain",
    # "lock", "key", "pick", "hammer", "nail", "screw",
    # "screwdriver", "wrench", "pliers", "saw", "axe",
    # "shovel", "spade", "pick", "hoe", "rake", "scythe",
    # "sickle", "knife", "fork", "spoon", "ladle", "whisk",
    # "grater", "peeler", "masher", "tongs", "skewer",
    # "spit", "oven", "stove", "grill", "fire", "pot",
    # "pan", "plate", "bowl", "cup", "mug", "glass",
    # "pitcher", "lamp", "candle", "torch", "lantern",
    # "oil", "flint", "steel", "tinder", "rope", "chain", "lock",
    # "key", "pick", "hammer", "nail", "screw", "screwdriver",
    # "wrench", "pliers", "saw", "axe", "shovel", "spade", "pick", "hoe",
    # "rake", "scythe", "sickle", "knife", "fork", "spoon", "ladle", "whisk",
    # "grater", "peeler", "masher", "tongs", "skewer", "spit", "oven", "stove",
    # "grill", "fire", "pot", "pan", "plate", "bowl", "cup"
