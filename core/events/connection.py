import jsonpickle
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService
from utilities.events import EventUtility


class ConnectionEvent(WebsocketInterface):
    """this is an event from connection.py to world.py using asyncio queues"""

    type = None
    message = ""

    def __init__(self, message, event_type):
        self.type = EventUtility.get_event_type_id(event_type)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)