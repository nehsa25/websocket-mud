import jsonpickle
from core.enums.events import EventEnum
from core.interfaces.event import EventInterface
from utilities.events import EventUtility


class HealthEvent(EventInterface):
    type = None
    name = ""
    current_hp = (0,)
    max_hp = (0,)
    attributes = []
    statuses = []

    def __init__(self, name, current_hp, max_hp, attributes, statuses):
        self.type = EventUtility.get_event_type_id(EventEnum.HEALTH)
        self.name = name
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.attributes = attributes
        self.statuses = statuses

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))