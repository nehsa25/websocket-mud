import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService

class NewConnectionEvent(WebsocketInterface):
    """this is the first event of a new connection"""

    type = None
    message = ""
    websocket = None

    def __init__(self, websocket):
        self.type = EventEnum.CONNECTION_NEW.value
        self.websocket = websocket

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)