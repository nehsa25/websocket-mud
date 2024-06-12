from enum import Enum
from monsters import Monsters
from muddirections import MudDirections

class Room:
    class Environments(Enum):
        TOWNSMEE = 1,
        BEACH = 2,
        FOREST = 3,
        JUNGLE = 4,
        BREACH = 5
    dirs = MudDirections()
    monsters = Monsters()
    id: 0
    name = ""
    description = ""
    exits = [ ],
    items = [],
    hidden_items = [],
    monsters = [],
    players = [],
    environment = None
    
    def __init__(id, name, description, exits, items, hidden_items, monsters, players, ) -> None:
        pass