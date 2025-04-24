import jsonpickle
from game.enums.events import Events
from utilities.events import EventUtility


class HelpEvent:
    type = None
    help_commands = []

    def __init__(self, help_commands):
        self.type = EventUtility.get_event_type_id(Events.HELP)
        self.help_commands = help_commands

    def to_json(self):
        return jsonpickle.encode(self)
