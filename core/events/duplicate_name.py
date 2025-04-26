import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class DuplicateNameEvent:
    type = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(EventEnum.DUPLICATE_NAME)

    def to_json(self):
        return jsonpickle.encode(self)
