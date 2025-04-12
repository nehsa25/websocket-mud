from enum import Enum
import json

import jsonpickle
from log_utils import LogUtils

class MudEvents:
    def __init__(self) -> None:
        pass

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
        MONSTER_IMAGE = 24
        PLAYER_IMAGE = 25
        NPC_IMAGE = 26
        ITEM_IMAGE = 27
        INVALID_NAME = 28
        USERNAME_CHANGED = 29

        @staticmethod
        def get_event_type_id(event):
            return event.value
        
    class EventEvent:
        type = None
        message = ""
        races = []
        extra = ""

        def __init__(self, type, message, extra):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.EVENT
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
        players = []
        npcs = []

        def __init__(self, name, description, items, exits, monsters, players, npcs) -> None:
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.ROOM
            )
            self.name = name
            self.description = description
            self.items = items
            self.exits = exits
            self.monsters = monsters
            self.players = players
            self.npcs = npcs

        def to_json(self):
            return jsonpickle.encode(self)
        
    class DuplicateNameEvent:
        type = None

        def __init__(self):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.DUPLICATE_NAME
            )

        def to_json(self):
            return jsonpickle.encode(self)
        
    class InvalidNameEvent:
        type = None

        def __init__(self):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.INVALID_NAME
            )

        def to_json(self):
            return jsonpickle.encode(self)

    class UsernameRequestEvent:
        world_name = ""
        type = None

        def __init__(self, world_name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.USERNAME_REQUEST
            )
            self.world_name = world_name

        def to_json(self):
            return jsonpickle.encode(self)
        
    class UsernameChangedEvent:
        type = None
        name = ""
        message = ""

        def __init__(self, message, name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.USERNAME_CHANGED
            )
            self.name = name
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class NewUserEvent:
        type = None
        races = None

        def __init__(self):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.USERNAME_REQUEST
            )
            # self.races = Races()

        def to_json(self):
            return jsonpickle.encode(self)

    class GetClientEvent:
        type = None
        players = None

        def __init__(self, number_players):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.CLIENT_LIST
            )
            self.players = number_players

        def to_json(self):
            return jsonpickle.encode(self)

    class WelcomeEvent:
        type = None
        message = ""
        name = ""

        def __init__(self, message, name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.WELCOME
            )
            self.name = name
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class TimeEvent:
        type = None
        message = ""

        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.TIME
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
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.REST
            )
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class HealthEvent:
        type = None
        name = ""
        current_hp = 0,         
        max_hp = 0, 
        attributes = []
        statuses = []

        def __init__(self, name, current_hp, max_hp, attributes, statuses):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.HEALTH
            )
            self.name = name
            self.current_hp = current_hp
            self.max_hp = max_hp
            self.attributes = attributes
            self.statuses = statuses

        def to_json(self):
            return jsonpickle.encode(self)

    class HelpEvent:
        type = None
        help_commands = []

        def __init__(self, help_commands):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.HELP
            )
            self.help_commands = help_commands

        def to_json(self):
            return jsonpickle.encode(self)
        
    class InventoryEvent:
        type = None
        inventory = None

        def __init__(self, inventory):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.INVENTORY
            )
            self.inventory = inventory

        def to_json(self):
            return jsonpickle.encode(self)

    class CommandEvent:
        type = None
        message = ""

        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.COMMAND
            )
            self.message = message

        def to_json(self):
            return jsonpickle.encode(self)

    class MapEvent:
        type = None
        map_image_name = ""
        def __init__(self, map_image_name, map_image_name_mini):
            self.type = MudEvents.EventTypes.get_event_type_id(MudEvents.EventTypes.MAP_EVENT)
            self.map_image_name = map_image_name
            self.map_image_name_mini = map_image_name_mini
        def to_json(self):
            return jsonpickle.encode(self)

    class RoomImageEvent:
        type = None
        room_image_name = ""
        def __init__(self, image_name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.ROOM_IMAGE
            )
            self.room_image_name = image_name
        def to_json(self):
            return jsonpickle.encode(self)

    class MonsterImageEvent:
        type = None
        image_name = ""
        def __init__(self, image_name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.MONSTER_IMAGE
            )
            self.image_name = image_name
        def to_json(self):
            return jsonpickle.encode(self)

    class PlayerImageEvent:
        type = None
        image_name = ""
        def __init__(self, image_name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.PLAYER_IMAGE
            )
            self.image_name = image_name
        def to_json(self):
            return jsonpickle.encode(self)

    class NpcImageEvent:
        type = None
        image_name = ""
        def __init__(self, image_name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.NPC_IMAGE
            )
            self.image_name = image_name
        def to_json(self):
            return jsonpickle.encode(self)

    class ItemImageEvent:
        type = None
        image_name = ""
        def __init__(self, image_name):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.ITEM_IMAGE
            )
            self.image_name = image_name
        def to_json(self):
            return jsonpickle.encode(self)
        
    class DirectionEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.DIRECTION
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class AttackEvent:
        type = None
        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.ATTACK
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class InfoEvent:
        type = None
        message = ""
        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.INFO
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class AnnouncementEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.ANNOUCEMENT
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)
    
    class EnvironmentEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.ENVIRONMENT
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)

    class ErrorEvent:
        type = None
        image_name = ""
        def __init__(self, message):
            self.type = MudEvents.EventTypes.get_event_type_id(
                MudEvents.EventTypes.ERROR
            )
            self.message = message
        def to_json(self):
            return jsonpickle.encode(self)
