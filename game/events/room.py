import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class RoomEvent:
    type = None
    name = ""
    description = ""
    items = []
    exits = []
    monsters = []
    players = []
    npcs = []

    def __init__(
        self, name, description, items, exits, monsters, players, npcs
    ) -> None:
        self.type = EventUtility.get_event_type_id(Events.ROOM)
        self.name = name
        self.description = description
        self.items = items
        self.exits = exits
        self.monsters = monsters
        self.players = players
        self.npcs = npcs

    def to_json(self):
        return jsonpickle.encode(self)
