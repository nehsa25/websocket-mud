import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from utilities.events import EventUtility


class GetClientEvent(EventInterface):
    type = None
    players = None

    def __init__(self, number_players):
        self.type = EventUtility.get_event_type_id(EventEnum.CLIENT_LIST)
        self.players = number_players

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER):
        # await EventService.instance().send_event(self, scope, websocket)
        pass