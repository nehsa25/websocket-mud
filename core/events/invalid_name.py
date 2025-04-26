import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class InvalidNameEvent:
    type = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(EventEnum.INVALID_NAME)

    def to_json(self):
        return jsonpickle.encode(self)
