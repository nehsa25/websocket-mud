import jsonpickle
from core.data.character_data import CharacterData
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService
from utilities.events import EventUtility


class WelcomeEvent(WebsocketInterface):
    type = None
    token = None
    character = None

    def __init__(self, character: CharacterData, token=None):
        self.type = EventUtility.get_event_type_id(EventEnum.WELCOME)
        self.name = character.name
        self.token = token
        self.character = character

    @property
    def message(self):
        return f"Welcome {self.name}!"

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)
        