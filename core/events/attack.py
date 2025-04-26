import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class AttackEvent:
    type = None

    def __init__(self, message):
        self.type = EventUtility.get_event_type_id(EventEnum.ATTACK)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)
