import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class InvalidNameEvent:
    type = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(Events.INVALID_NAME)

    def to_json(self):
        return jsonpickle.encode(self)
