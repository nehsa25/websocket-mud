import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService
from utilities.events import EventUtility


class RestEvent(WebsocketInterface):
    type = None
    message = ""
    is_resting = False
    rest_error = False

    def __init__(self, message, rest_error=False, is_resting=False):
        self.rest_error = rest_error
        self.is_resting = is_resting
        self.type = EventUtility.get_event_type_id(EventEnum.REST)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)