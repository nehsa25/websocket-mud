import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from services.events import EventService
from services.auth import AuthService
from utilities.events import EventUtility


class WelcomeEvent(EventInterface):
    type = None
    message = ""
    name = ""
    token = None

    def __init__(self, message, name, token=None):
        self.type = EventUtility.get_event_type_id(EventEnum.WELCOME)
        self.name = name
        self.message = message
        
        if token is None:
            self.token = AuthService.generate_token(name)

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)
        