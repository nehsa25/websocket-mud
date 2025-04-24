import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class GetClientEvent:
    type = None
    players = None

    def __init__(self, number_players):
        self.type = EventUtility.get_event_type_id(Events.CLIENT_LIST)
        self.players = number_players

    def to_json(self):
        return jsonpickle.encode(self)
