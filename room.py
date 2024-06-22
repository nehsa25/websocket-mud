
import asyncio
import inspect
import time
from aiimages import AIImages
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class MudDirections:# directions
    up = ('u', 'Up')
    down = ('d', 'Down')
    north = ('n', 'North')
    south = ('s', 'South')
    east = ('e', 'East')
    west = ('w', 'West')
    northwest = ('nw', 'Northwest')
    northeast = ('ne', 'Northeast')
    southeast = ('se', 'Southeast')
    southwest = ('sw', 'Southwest')
    directions = [
        up[0].lower(), 
        up[1].lower(), 
        down[0].lower(), 
        down[1].lower(), 
        north[0].lower(), 
        north[1].lower(), 
        south[0].lower(), 
        south[1].lower(), 
        east[0].lower(), 
        east[1].lower(), 
        west[0].lower(), 
        west[1].lower(), 
        northwest[0].lower(), 
        northwest[1].lower(), 
        northeast[0].lower(), 
        northeast[1].lower(), 
        southeast[0].lower(), 
        southeast[1].lower(), 
        southwest[0].lower(), 
        southwest[1].lower()
    ]
    pretty_directions = [up, down, north, south, east, west, northwest, northeast, southeast, southwest]

    opp_directions = [
        (up, down), 
        (east, west),
        (north, south),
        (northeast, southwest),
        (northwest, southeast)
    ]
    
class Room(Utility):
    dirs = MudDirections()
    id: 0
    name = ""
    inside = False
    description = ""
    environment = None,
    exits = [],
    items = [],
    hidden_items = [],
    monsters = [],
    players = [],
    npcs = [] 
     
    def __init__(self, id, name, inside, description, exits, environment, logger, items=[], hidden_items=[], monsters=[], players=[], npcs=[]) -> None:
        self.id = id
        self.name = name
        self.inside = inside
        self.description = description
        self.exits = exits
        self.environment = environment
        self.items = items
        self.hidden_items = hidden_items
        self.monsters = monsters
        self.players = players
        self.npcs = npcs
        self.logger = logger
        LogUtils.debug(f"Initializing RoomFactory() class", self.logger)

    async def alert_room(self, message, exclude_player=False, player=None, event_type=MudEvents.InfoEvent):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, message: {message}", self.logger)
        for p in self.players:
            if exclude_player and player is not None:
                if p.name != player.name:
                    LogUtils.info(f"{method_name}: alerting {p.name} of \"{message}\"", self.logger)
                    await self.send_message(event_type(message), p.websocket)
            else:
                await self.send_message(event_type(message), p.websocket)

    # returns player, world
    async def process_room(self, player, world, look_location_id = None):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        new_room = self
        if look_location_id is not None:
            new_room = world.environments.all_rooms[look_location_id]

        # get the description        
        if new_room.inside:
            description = new_room.description
        else:
            description = world.world_events.weather.add_weather_description(new_room.description)

        # show items
        items = ""
        if len(new_room.items) > 0:
            for item in new_room.items:
                items += item.name + ", "
            items = items[0 : len(items) - 2]

        # offer possible exits
        exits = ""
        for available_exit in new_room.exits:
            exits += available_exit["direction"][1] + ", "
        exits = exits[0 : len(exits) - 2]

        # show monsters
        monsters = ""
        for monster in new_room.monsters:
            monsters += monster.name + ", "
        monsters = monsters[0 : len(monsters) - 2]

        # show people
        people = ""
        for p in world.players.players:
            if player.name == p.name:
                continue
            if p.room.id == player.room.id:
                people += p.name + ", "
        if people != "":
            people = people[0 : len(people) - 2]

        # formulate message to client
        json_msg = MudEvents.RoomEvent(
            new_room.name, description, items, exits, monsters, people
        )

        LogUtils.debug(f"Sending json: {json_msg}", self.logger)
        await self.send_message(json_msg, player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world

class RoomFactory(Utility):
    environment = None
    
    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug(f"Initializing Room() class", self.logger)


    def add_room(self, id, name, inside, description, exits, environment, items=[], hidden_items=[], monsters=[], players=[], npcs=[]):
        method_name = inspect.currentframe().f_code.co_name
        room = Room(id, name, inside, description, exits, environment, items=[], hidden_items=[], monsters=[], players=[], npcs=[], logger=self.logger)
        LogUtils.debug(f"{method_name}: generated room: {room}", self.logger)
        return room


