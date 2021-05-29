from monsters import Monsters
from items import Items
from muddirections import MudDirections

class Rooms:
    dirs = MudDirections()
    monsters = Monsters()
    rooms = [
        { 
            "id": 0,
            "name": "Beach",
            "description": "You are on a white-sand beach.  You see paths leading off in several directions.",
            "exits": [ 
                    { "direction": dirs.west, "id": 1 },
                    { "direction": dirs.north, "id": 2 },
                    { "direction": dirs.northeast, "id": 3 },
                    { "direction": dirs.east, "id": 4 },
                    { "direction": dirs.south, "id": 5 }
                ],
            "items": [Items.helmet, Items.stick, Items.maul],
            "hidden_items": [],
            "monsters": [monsters.get_crab(), monsters.get_zombie_surfer()],
            "players": []          
        },
        { 
            "id": 1,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [ { "direction": dirs.east, "id": 0 } ],
            "items": [],
            "hidden_items": [Items.shovel],
            "monsters": [monsters.get_skeleton(), monsters.get_skeleton(), monsters.get_zombie(), monsters.get_ghoul()],
            "players": []          
        },
        { 
            "id": 2,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [ 
                    { "direction": dirs.south, "id": 0 },
                    { "direction": dirs.northeast, "id": 6 } ],
            "items": [Items.shovel],
            "hidden_items": [],
            "monsters": [monsters.get_skeleton(), monsters.get_skeleton()],
            "players": []          
        },
        { 
            "id": 3,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [ 
                    { "direction": dirs.southwest, "id": 0 }, 
                    { "direction": dirs.south, "id": 4 },
                    { "direction": dirs.north, "id": 6} ],
            "items": [],
            "hidden_items": [Items.lockpick],
            "monsters": [monsters.get_zombie_surfer()],
            "players": []          
        },
        { 
            "id": 4,
            "name": "Beach",
            "description": "You are on a white-sand beach.",
            "exits": [ 
                    { "direction": dirs.west, "id": 0 }, 
                    { "direction": dirs.northeast, "id": 3 } ],
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": []          
        },
        { 
            "id": 5,
            "name": "Beach Shore",
            "description": "You are on a white sandy beach shore.  Green ocean surrounds you in all directions except for the North.  There's an odd tension in the air.",
            "exits": [ 
                    { "direction": dirs.north, "id": 0 }
                ],
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": []          
        },
        { 
            "id": 6,
            "name": "Beachside Church",
            "description": "You are at the entrance of an old forgotten church.  There's a lock on the door.",
            "exits": [ 
                    { "direction": dirs.south, "id": 3 }, 
                    { "direction": dirs.southwest, "id": 2 } ],
            "items": [],
            "hidden_items": [],
            "monsters": [monsters.get_thug()],
            "players": []          
        }
    ]