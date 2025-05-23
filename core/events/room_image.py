import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService
from utilities.events import EventUtility


class RoomImageEvent(WebsocketInterface):
    type = None
    room_image_name = ""

    def __init__(self, image_name):
        self.type = EventUtility.get_event_type_id(EventEnum.ROOM_IMAGE)
        self.room_image_name = image_name

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)