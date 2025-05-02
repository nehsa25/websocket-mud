import jsonpickle
from utilities.events import EventUtility


class ConnectionEvent:
    """this is an event from connection.py to world.py using asyncio queues"""

    type = None
    message = ""

    def __init__(self, message, event_type):
        self.type = EventUtility.get_event_type_id(event_type)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)
