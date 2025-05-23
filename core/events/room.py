import jsonpickle
from core.data.room_data import RoomData
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.websocket import WebsocketInterface
from services.events import EventService
from utilities.events import EventUtility


class RoomEvent(WebsocketInterface):
    type = None
    name = ""
    description = ""
    items = []
    exits = []
    monsters = []
    players = []
    npcs = []

    def __init__(
        self, room: RoomData
    ) -> None:
        self.type = EventUtility.get_event_type_id(EventEnum.ROOM)
        self.room: RoomData = room

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)