import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class RestEvent:
    type = None
    message = ""
    is_resting = False
    rest_error = False

    def __init__(self, message, rest_error=False, is_resting=False):
        self.rest_error = rest_error
        self.is_resting = is_resting
        self.type = EventUtility.get_event_type_id(Events.REST)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)
