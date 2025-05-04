import jsonpickle
from core.enums.events import EventEnum
from core.interfaces.event import EventInterface
from utilities.auth import Auth
from utilities.events import EventUtility


class WelcomeEvent(EventInterface):
    type = None
    message = ""
    name = ""

    def __init__(self, message, name):
        self.type = EventUtility.get_event_type_id(EventEnum.WELCOME)
        self.name = name
        self.message = message
        self.token = Auth.generate_token(name)

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))