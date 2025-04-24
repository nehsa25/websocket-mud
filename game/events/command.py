import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class CommandEvent:
    type = None
    message = ""

    def __init__(self, message):
        self.type = EventUtility.get_event_type_id(Events.COMMAND)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)
