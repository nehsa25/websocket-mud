import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class ClientMessageEvent:
    type = None
    message = None
    websocket = None

    def __init__(self, message, websocket):
        self.type = EventUtility.get_event_type_id(EventEnum.CLIENT_MESSAGE)
        self.message = message
        self.websocket = websocket

    def to_json(self):
        return jsonpickle.encode(self)
