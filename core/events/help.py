import jsonpickle
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from services.events import EventService
from utilities.events import EventUtility


class HelpEvent(EventInterface):
    type = None
    help_commands = []

    def __init__(self, help_commands):
        self.type = EventUtility.get_event_type_id(EventEnum.HELP)
        self.help_commands = help_commands

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket, scope=SendScopeEnum.PLAYER):
        await EventService.instance().send_event(self, scope, websocket)