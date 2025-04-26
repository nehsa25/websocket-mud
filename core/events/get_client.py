import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class GetClientEvent:
    type = None
    players = None

    def __init__(self, number_players):
        self.type = EventUtility.get_event_type_id(EventEnum.CLIENT_LIST)
        self.players = number_players

    def to_json(self):
        return jsonpickle.encode(self)
