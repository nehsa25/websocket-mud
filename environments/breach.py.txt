from environments import Environments
from monsters import Monsters
from items import Items
from muddirections import MudDirections
from room import Room

class Breach:
    rooms = [
        {
            "id": 15,
            "name": "Breach",
            "description": "Ethereal violet and blue fog surrounds everything.  It's eerie quiet.",
            "exits": [
                {"direction": Room.dirs.north, "id": 17},
                {"direction": Room.dirs.east, "id": 19},
                {"direction": Room.dirs.west, "id": 20},
            ],
            "environment": Environments.BREACH,
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
        },
        {
            "id": 16,
            "name": "Breach",
            "description": "Ethereal violet and blue fog surrounds everything.  It's eerie quiet.",
            "exits": [{"direction": Room.dirs.west, "id": 18}],
            "environment": Environments.BREACH,
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
        },
        {
            "id": 17,
            "name": "Breach",
            "description": "Ethereal violet and blue fog surrounds everything.  It's eerie quiet.",
            "exits": [{"direction": Room.dirs.east, "id": 18}],
            "environment": Environments.BREACH,
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
        },
        {
            "id": 18,
            "name": "Breach",
            "description": "Ethereal violet and blue fog surrounds everything.  It's eerie quiet.",
            "exits": [{"direction": Room.dirs.south, "id": 22}],
            "environment": Environments.BREACH,
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
        },
        {
            "id": 19,
            "name": "Breach",
            "description": "Ethereal violet and blue fog surrounds everything.  It's eerie quiet.",
            "exits": [
                {"direction": Room.dirs.north, "id": 21},
                {"direction": Room.dirs.east, "id": 23},
            ],
            "environment": Environments.BREACH,
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
        },
        {
            "id": 20,
            "name": "Breach",
            "description": "Ethereal violet and blue fog surrounds everything.  It's eerie quiet.",
            "exits": [{"direction": Room.dirs.west, "id": 22}],
            "environment": Environments.BREACH,
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
        },
        {
            "id": 21,
            "name": "Breach",
            "description": "Ethereal violet and blue fog surrounds everything.  It's eerie quiet.",
            "exits": [{"direction": Room.dirs.south, "id": 25}],
            "environment": Environments.BREACH,
            "items": [],
            "hidden_items": [],
            "monsters": [],
            "players": [],
        }
    ]