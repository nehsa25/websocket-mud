from enum import Enum
import json

import jsonpickle
from log_utils import LogUtils
from race import Races

class MudEvents:
    def __init__(self) -> None:
        pass

    class EventUtility:
        logger = None

        def __init__(self, logger) -> None:
            self.logger = logger
            LogUtils.debug(f"Initializing Event() class", self.logger)

        class EventTypes(Enum):
            NONE = -1
            DUPLICATE_NAME = 0
            EVENT = 1
            WELCOME = 2
            ERROR = 3
            INFO = 4
            ROOM = 5
            COMMAND = 6
            USERNAME_REQUEST = 7
            USERNAME_ANSWER = 8
            BOOK = 9
            TIME = 10
            CHANGE_NAME = 11
            YOU_ATTACK = 12
            INVENTORY = 13
            ATTACK = 14
            HEALTH = 15
            CLIENT_LIST = 16
            MAP_EVENT = 17
            ROOM_IMAGE = 18
            DIRECTION = 19
            ANNOUCEMENT = 20
            ENVIRONMENT = 21
            REST = 22
            HELP = 23

        @staticmethod
        def get_event_type_id(event):
            return event.value

    class EventEvent:
        type = None
        message = ""
        races = []
        extra = ""

        def __init__(self, type, message, extra):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.EVENT
            )
            self.type = type
            self.message = message
            self.extra = extra

        def to_json(self):
            return jsonpickle.encode(self)

    class RoomEvent:
        type = None
        name = ""
        description = ""
        items = []
        exits = []
        monsters = []
        people = []

        def __init__(self, name, description, items, exits, monsters, people) -> None:
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.ROOM
            )
            self.name = name
            self.description = description
            self.items = items
            self.exits = exits
            self.monsters = monsters
            self.people = people

        def to_json(self):
            return jsonpickle.encode(self)

    class DuplicateNameEvent:
        type = None

        def __init__(self):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.DUPLICATE_NAME
            )

        def to_json(self):
            return jsonpickle.encode(self)

    class UsernameRequestEvent:
        world_name = ""
        type = None

        def __init__(self, world_name):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.USERNAME_REQUEST
            )
            self.world_name = world_name

        def to_json(self):
            return jsonpickle.encode(self)

    class NewUserEvent:
        type = None
        races = None

        def __init__(self):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.USERNAME_REQUEST
            )
            self.races = Races()

        def to_json(self):
            return jsonpickle.encode(self)

    class GetClientEvent:
        type = None
        players = None

        def __init__(self, number_players):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.CLIENT_LIST
            )
            self.players = number_players

        def to_json(self):
            return jsonpickle.encode(self)

    class WelcomeEvent:
        type = None
        message = ""

        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.WELCOME
            )
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class TimeEvent:
        type = None
        message = ""

        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.TIME
            )
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class RestEvent:
        type = None
        message = ""
        is_resting = False
        rest_error = False

        def __init__(self, message, rest_error = False, is_resting = False):
            self.rest_error = rest_error
            self.is_resting = is_resting
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.REST
            )
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class HealthEvent:
        type = None
        message = ""
        is_resting = None

        def __init__(self, message, is_resting = False):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.HEALTH
            )
            self.message = message
            self.is_resting = is_resting

        def to_json(self):
            return jsonpickle.encode(self)

    class HelpEvent:
        type = None
        help_commands = []

        def __init__(self, help_commands):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.HELP
            )
            self.help_commands = help_commands

        def to_json(self):
            return jsonpickle.encode(self)
        
    class InventoryEvent:
        type = None
        inventory = None

        def __init__(self, inventory):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.INVENTORY
            )
            self.inventory = inventory

        def to_json(self):
            return jsonpickle.encode(self)

    class CommandEvent:
        type = None
        message = ""

        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.COMMAND
            )
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class MapEvent:
        type = None
        map_image_name = ""
        def __init__(self, map_image_name):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.MAP_EVENT
            )
            self.map_image_name = map_image_name
        def to_json(self):
            return jsonpickle.encode(self)

    class RoomImageEvent:
        type = None
        room_image_name = ""
        def __init__(self, image_name):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.ROOM_IMAGE
            )
            self.room_image_name = image_name
        def to_json(self):
            return jsonpickle.encode(self)

    class DirectionEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.DIRECTION
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class AttackEvent:
        type = None
        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.ATTACK
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class InfoEvent:
        type = None
        message = ""
        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.INFO
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class AnnouncementEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.ANNOUCEMENT
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)
    
    class EnvironmentEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.ENVIRONMENT
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class ErrorEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.ERROR
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)




