import jsonpickle
from core.enums.events import EventEnum
from core.interfaces.event import EventInterface
from utilities.events import EventUtility


class InvalidTokenEvent(EventInterface):
    type = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(EventEnum.INVALID_TOKEN)

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))
