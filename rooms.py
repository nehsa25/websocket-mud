from monsters import Monsters
from items import Items
from muddirections import MudDirections

class Rooms:
    dirs = MudDirections()
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
                    { "direction": dirs.down, "id": 5 }
                ],
            "items": [Items.helmet, Items.stick, Items.maul],
            "hidden_items": [],
            "monsters": [Monsters.get_crab()],
            "players": []          
        },
        { 
            "id": 1,
            "name": "Graveyard",
            "description": "You are in a dark, gloomy graveyard, lit only by moonlight.",
            "exits": [ { "direction": dirs.east, "id": 0 } ],
            "items": [],
            "hidden_items": [Items.shovel],
            "monsters": [Monsters.get_skeleton(), Monsters.get_skeleton(), Monsters.get_zombie(), Monsters.get_ghoul()],
            "players": []          
        },
        { 
            "id": 2,
            "name": "Graveyard",
            "description": "You are in a dark, gloomy graveyard, lit only by moonlight.  You see a gravestone.",
            "exits": [ 
                    { "direction": dirs.south, "id": 0 },
                    { "direction": dirs.northeast, "id": 6 } ],
            "items": [Items.shovel],
            "hidden_items": [],
            "monsters": [Monsters.get_skeleton(), Monsters.get_skeleton()],
            "players": []          
        },
        { 
            "id": 3,
            "name": "Graveyard",
            "description": "You are in a dark, gloomy graveyard, lit only by moonlight.",
            "exits": [ 
                    { "direction": dirs.southwest, "id": 0 }, 
                    { "direction": dirs.south, "id": 4 },
                    { "direction": dirs.north, "id": 6} ],
            "items": [],
            "hidden_items": [Items.lockpick],
            "monsters": [],
            "players": []          
        },
        { 
            "id": 4,
            "name": "Graveyard",
            "description": "You are in a dark, gloomy graveyard, lit only by moonlight.",
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
            "name": "Crypt",
            "description": "You are in a dark room.  A staircase leads up.",
            "exits": [ 
                    { "direction": dirs.up, "id": 0 }
                ],
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": []          
        },
        { 
            "id": 6,
            "name": "Church",
            "description": "You are at the entrance of a church.",
            "exits": [ 
                    { "direction": dirs.south, "id": 3 }, 
                    { "direction": dirs.southwest, "id": 2 } ],
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": []          
        }
    ]