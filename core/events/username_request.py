import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService
from utilities.events import EventUtility


class UsernameRequestEvent(WebsocketInterface):
    world_name = ""
    type = None

    def __init__(self, world_name):
        self.type = EventUtility.get_event_type_id(EventEnum.USERNAME_REQUEST)
        self.world_name = world_name

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)