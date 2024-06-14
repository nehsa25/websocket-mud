from enum import Enum
import json

import jsonpickle
from log_utils import LogUtils
from race import Races

class MudEvents:
    class Event(Enum):
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
    
    def get_event_type_id(event):
        return event.value
        
class MudEvent(MudEvents):
    type = None
    message = ""
    races = []
    extra = ""
    
    def __init__(self, type, message, extra):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.EVENT)
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
        self.type = MudEvents.get_event_type_id(MudEvents.Event.ROOM)
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
        self.type = MudEvents.get_event_type_id(MudEvents.Event.DUPLICATE_NAME)
        
    def to_json(self):
        return jsonpickle.encode(self)

class UsernameRequestEvent:
    type = None
    def __init__(self):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.USERNAME_REQUEST)
        
    def to_json(self):
        return jsonpickle.encode(self)
    
class NewUserEvent:
    type = None
    races = None
    def __init__(self):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.USERNAME_REQUEST)
        self.races = Races()
        
    def to_json(self):
        return jsonpickle.encode(self)

class GetClientEvent:
    type = None
    players = None
    def __init__(self, number_players):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.CLIENT_LIST)
        self.players = number_players

    def to_json(self):
        return jsonpickle.encode(self)

class WelcomeEvent:
    type = None
    message = ""
    def __init__(self, message):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.WELCOME)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

class TimeEvent:
    type = None
    message = ""
    def __init__(self, message):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.TIME)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

class HealthEvent:
    type = None
    message = ""
    def __init__(self, message):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.HEALTH)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

class InventoryEvent:
    type = None
    message = ""
    def __init__(self, message):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.INVENTORY)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

class CommandEvent:
    type = None
    message = ""
    def __init__(self, message):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.COMMAND)
        self.message = message

    def to_json(self):
        return jsonpickle.encode(self)

class MapEvent:
    type = None
    map_name = ""
    def __init__(self, map_name):
        self.type = MudEvents.get_event_type_id(MudEvents.Event.MAP_EVENT)
        self.map_name = map_name

    def to_json(self):
        return jsonpickle.encode(self)
