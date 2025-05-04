import jsonpickle

from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from services.events import EventService
from ..enums.events import EventEnum
from utilities.events import EventUtility


class MonsterImageEvent(EventInterface):
    type = None
    image_name = ""

    def __init__(self, image_name):
        self.type = EventUtility.get_event_type_id(EventEnum.MONSTER_IMAGE)
        self.image_name = image_name

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER):
        await EventService.instance().send_event(self, scope, websocket)