import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class DirectionEvent:
    type = None
    image_name = ""

    def __init__(self, message):
        self.type = EventUtility.get_event_type_id(EventEnum.DIRECTION)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)
