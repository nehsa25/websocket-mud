import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from services.events import EventService
from utilities.events import EventUtility


class NewUserEvent(EventInterface):
    type = None
    races = None

    def __init__(self):
        self.type = EventUtility.get_event_type_id(EventEnum.USERNAME_REQUEST)

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER):
        await EventService.instance().send_event(self, scope, websocket)