import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class NewUserEvent:
    type = None
    races = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(EventEnum.USERNAME_REQUEST)

    def to_json(self):
        return jsonpickle.encode(self)
