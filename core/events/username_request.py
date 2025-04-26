import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class UsernameRequestEvent:
    world_name = ""
    type = None

    def __init__(self, world_name):
        self.type = EventUtility.get_event_type_id(EventEnum.USERNAME_REQUEST)
        self.world_name = world_name

    def to_json(self):
        return jsonpickle.encode(self)
