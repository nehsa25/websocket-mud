from items import Items
from room import Room
from monsters import Monsters

class Beach:
    monsters = Monsters()
    rooms = [
        {
            "id": 6,
            "name": "Beach",
            "description": "You are on a white-sand beach.  You see paths leading off in several directions.",
            "exits": [
                {"direction": Room.dirs.west, "id": 1},
                {"direction": Room.dirs.north, "id": 2},
                {"direction": Room.dirs.northeast, "id": 3},
                {"direction": Room.dirs.east, "id": 4},
                {"direction": Room.dirs.south, "id": 5},
            ],
            "items": [Items.helmet, Items.stick, Items.maul],
            "hidden_items": [],
            "monsters": [],
            "players": [],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 7,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [{"direction": Room.dirs.east, "id": 0}],
            "items": [],
            "hidden_items": [Items.shovel],
            "monsters": [
                monsters.get_skeleton(),
                monsters.get_skeleton(),
                monsters.get_zombie(),
                monsters.get_ghoul(),
            ],
            "players": [],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 8,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [
                {"direction": Room.dirs.south, "id": 0},
                {"direction": Room.dirs.northeast, "id": 6},
            ],
            "items": [Items.shovel],
            "hidden_items": [],
            "monsters": [monsters.get_skeleton(), monsters.get_skeleton()],
            "players": [],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 9,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [
                {"direction": Room.dirs.southwest, "id": 0},
                {"direction": Room.dirs.south, "id": 4},
                {"direction": Room.dirs.north, "id": 6},
            ],
            "items": [],
            "hidden_items": [Items.lockpick],
            "monsters": [monsters.get_zombie_surfer()],
            "players": [],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 10,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [
                {"direction": Room.dirs.west, "id": 0},
                {"direction": Room.dirs.northeast, "id": 3},
            ],
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 11,
            "name": "Beach Shore",
            "description": "You are on a white sandy beach shore.  Green ocean surrounds you in all directions except for the North.  There's an odd tension in the air.",
            "exits": [{"direction": Room.dirs.north, "id": 0}],
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 12,
            "name": "Beachside Church",
            "description": "You are at the entrance of an old forgotten church.  There's a lock on the door.",
            "exits": [
                {"direction": Room.dirs.south, "id": 3},
                {"direction": Room.dirs.southwest, "id": 2},
            ],
            "items": [],
            "hidden_items": [],
            "monsters": [monsters.get_thug()],
            "players": [],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 13,
            "name": "Church Interior",
            "description": "You are inside the church.  The pews are dusty and the air is musty.",
            "exits": [
                {"direction": Room.dirs.north, "id": 6},
                {"direction": Room.dirs.up, "id": 8},
            ],
            "environment": Room.Environments.BEACH
        },
        {
            "id": 14,
            "name": "Church Bell Tower",
            "description": "You are in the bell tower of the church.  The bell is missing.",
            "exits": [{"direction": Room.dirs.down, "id": 7}],
            "environment": Room.Environments.BEACH
        },
    ]
