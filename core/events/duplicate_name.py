import jsonpickle
from core.enums.events import EventEnum
from core.interfaces.event import EventInterface
from utilities.events import EventUtility


class DuplicateNameEvent(EventInterface):
    type = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(EventEnum.DUPLICATE_NAME)

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))