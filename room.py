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
    npcs = [],
    environment = None
    
    def __init__(self, id, name, description, exits, environment, items=[], hidden_items=[], monsters=[], players=[], npcs=[]) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits
        self.items = items
        self.hidden_items = hidden_items
        self.monsters = monsters
        self.players = players
        self.npcs = npcs
        self.environment = environment        
        pass