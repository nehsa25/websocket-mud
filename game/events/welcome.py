import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class WelcomeEvent:
    type = None
    message = ""
    name = ""

    def __init__(self, message, name):
        self.type = EventUtility.get_event_type_id(Events.WELCOME)
        self.name = name
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)
