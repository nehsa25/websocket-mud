import jsonpickle
from core.enums.events import EventEnum
from core.interfaces.event import EventInterface
from utilities.events import EventUtility


class InventoryEvent(EventInterface):
    type = None
    inventory = None

    def __init__(self, inventory):
        self.type = EventUtility.get_event_type_id(EventEnum.INVENTORY)
        self.inventory = inventory

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))