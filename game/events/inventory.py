import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class InventoryEvent:
    type = None
    inventory = None

    def __init__(self, inventory):
        self.type = EventUtility.get_event_type_id(Events.INVENTORY)
        self.inventory = inventory

    def to_json(self):
        return jsonpickle.encode(self)
