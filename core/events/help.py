import jsonpickle
from core.enums.events import EventEnum
from utilities.events import EventUtility


class HelpEvent:
    type = None
    help_commands = []

    def __init__(self, help_commands):
        self.type = EventUtility.get_event_type_id(EventEnum.HELP)
        self.help_commands = help_commands

    def to_json(self):
        return jsonpickle.encode(self)

    async def send(self, websocket):
        msg = self.to_json()
        await websocket.send(str(msg))