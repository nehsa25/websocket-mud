import jsonpickle
from core.enums.events import EventEnum

class NewConnectionEvent:
    """this is the first event of a new connection"""

    type = None
    message = ""
    websocket = None

    def __init__(self, websocket):
        self.type = EventEnum.CONNECTION_NEW.value
        self.websocket = websocket


    def to_json(self):
        return jsonpickle.encode(self)
