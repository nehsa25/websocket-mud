import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class MapEvent:
    type = None
    map_image_name = ""

    def __init__(self, map_image_name, map_image_name_mini):
        self.type = EventUtility.get_event_type_id(Events.MAP_EVENT)
        self.map_image_name = map_image_name
        self.map_image_name_mini = map_image_name_mini

    def to_json(self):
        return jsonpickle.encode(self)
