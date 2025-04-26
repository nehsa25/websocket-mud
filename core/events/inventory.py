import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class InventoryEvent:
    type = None
    inventory = None

    def __init__(self, inventory):
        self.type = EventUtility.get_event_type_id(EventEnum.INVENTORY)
        self.inventory = inventory

    def to_json(self):
        return jsonpickle.encode(self)
