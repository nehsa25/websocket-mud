import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from services.events import EventService
from utilities.events import EventUtility


class RoomEvent(EventInterface):
    type = None
    name = ""
    description = ""
    items = []
    exits = []
    monsters = []
    players = []
    npcs = []

    def __init__(
        self, name, description, items, exits, monsters, players, npcs
    ) -> None:
        self.type = EventUtility.get_event_type_id(EventEnum.ROOM)
        self.name = name
        self.description = description
        self.items = items
        self.exits = exits
        self.monsters = monsters
        self.players = players
        self.npcs = npcs

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER, exclude_player=False, player_data=None):
        await EventService.instance().send_event(self, scope, websocket, exclude_player, player_data)