import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class UsernameChangedEvent:
    type = None
    name = ""
    message = ""

    def __init__(self, message, name):
        self.type = EventUtility.get_event_type_id(EventEnum.USERNAME_CHANGED)
        self.name = name
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))