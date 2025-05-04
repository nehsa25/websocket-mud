import jsonpickle
from core.enums.events import EventEnum
from core.interfaces.event import EventInterface
from utilities.events import EventUtility


class AnnouncementEvent(EventInterface):
    type = None
    image_name = ""

    def __init__(self, message):
        self.type = EventUtility.get_event_type_id(EventEnum.ANNOUCEMENT)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))