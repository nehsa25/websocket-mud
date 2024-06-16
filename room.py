from muddirections import MudDirections

class Room:
    dirs = MudDirections()
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
