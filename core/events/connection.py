import jsonpickle
from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from services.events import EventService
from utilities.events import EventUtility


class ConnectionEvent(EventInterface) :
    """this is an event from connection.py to world.py using asyncio queues"""

    type = None
    message = ""

    def __init__(self, message, event_type):
        self.type = EventUtility.get_event_type_id(event_type)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER):
        await EventService.instance().send_event(self, scope, websocket)