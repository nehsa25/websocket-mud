import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class NpcImageEvent:
    type = None
    image_name = ""

    def __init__(self, image_name):
        self.type = EventUtility.get_event_type_id(Events.NPC_IMAGE)
        self.image_name = image_name

    def to_json(self):
        return jsonpickle.encode(self)
