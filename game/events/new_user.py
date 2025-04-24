import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class NewUserEvent:
    type = None
    races = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(Events.USERNAME_REQUEST)

    def to_json(self):
        return jsonpickle.encode(self)
