import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class PlayerImageEvent:
    type = None
    image_name = ""

    def __init__(self, image_name):
        self.type = EventUtility.get_event_type_id(EventEnum.PLAYER_IMAGE)
        self.image_name = image_name

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))