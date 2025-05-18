import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService
from utilities.events import EventUtility


class MapEvent(WebsocketInterface):
    type = None
    map_image_name = ""

    def __init__(self, map_image_name, map_image_name_mini):
        self.type = EventUtility.get_event_type_id(EventEnum.MAP_EVENT)
        self.map_image_name = map_image_name
        self.map_image_name_mini = map_image_name_mini

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)