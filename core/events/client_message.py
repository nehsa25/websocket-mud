import jsonpickle
from core.enums.events import EventEnum
from core.interfaces.event import EventInterface
from utilities.events import EventUtility


class ClientMessageEvent(EventInterface):
    type = None
    message = None
    websocket = None

    def __init__(self, message, websocket):
        self.type = EventUtility.get_event_type_id(EventEnum.CLIENT_MESSAGE)
        self.message = message
        self.websocket = websocket

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))