import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class TimeEvent:
    type = None
    message = ""

    def __init__(self, message):
        self.type = EventUtility.get_event_type_id(EventEnum.TIME)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)
