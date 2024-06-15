import asyncio
import datetime
from enum import Enum
import inspect
import os
import re
import time
import pydot
from random import randint
from environments import Environments
from mudevent import MapEvent, TimeEvent
from rooms import Rooms
from utility import Utility
from log_utils import LogUtils, Level
from command import Command

class World:   
    world_name = "Illisurom"
    players = []
    breeze_task = None
    rain_task = None
    eerie_task = None
    thunder_task = None
    mob_attack_task = None
    time_task = None
    logger = None
    utility = None
    command = None
    rooms = None
    rooms_list = None
    room_start = "Town Smee - "
    
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing World() class", self.logger)
        if self.utility is None:
            self.utility = Utility(self.logger)
            
        if self.command is None:
            self.command = Command(self.logger)
            
        if self.rooms is None:
            self.rooms = Rooms(self.world_name, self.logger)

    # schedule some events that'll do shit
    async def setup_world_events(self):        
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        if self.breeze_task == None:
            self.breeze_task = asyncio.create_task(self.breeze())
            
        if self.rain_task == None:
            self.rain_task = asyncio.create_task(self.rain())

        if self.eerie_task == None:
            self.eerie_task = asyncio.create_task(self.eerie_silence())

        if self.thunder_task == None:
            self.thunder_task = asyncio.create_task(self.thunder())

        if self.time_task == None:
            self.time_task = asyncio.create_task(self.get_system_time())

    # It begins to rain..
    async def rain(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 3600*2)
            LogUtils.debug(f"Will run rain1 event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("It begins to rain..", 'event', world_player.websocket)

            # wait for it to stop
            rand = randint(100, 500)
            LogUtils.debug(f"Will run rain2 event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("The rain pitter-patters to a stop and the sun begins to shine through the clouds..", 'event', world_player.websocket)

    # You hear thunder off in the distane..
    async def thunder(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 3800*2)
            LogUtils.debug(f"Will run thunder event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("You hear thunder off in the distance..", 'event', world_player.websocket)

    # A gentle breeze blows by you..
    async def breeze(self):    
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 3800*2)
            LogUtils.debug(f"Will run breeze event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("A gentle breeze blows by you..", 'event', world_player.websocket)

    # An eerie silence settles on the room..
    async def eerie_silence(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 4000*2)
            LogUtils.debug(f"Will run eerie_silence event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("An eerie silence settles on the room..", 'event', world_player.websocket)

    # responsible for moving a player from one room to the next
    async def move_room(self, new_room_id, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        old_room = await self.get_room(player.location_id)
        new_room = await self.get_room(new_room_id)

        if old_room != new_room:
            for monster in old_room.monsters:
                if monster.in_combat == player:
                    monster.in_combat = None

            # remove player from old room
            old_room.players.remove(player)

        # add player to new room        
        new_room.players.append(player)
        player.location_id = new_room.id

        # show new room
        player, world = await self.command.process_room(new_room_id, player, world)
        
        # generate new map
        await self.generate_map(player)
        
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player, world

    # just return the current date/time
    async def get_system_time(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            time = datetime.datetime.now().strftime("%I:%M%p on %B %d")
            for world_player in self.players:
                time_event = TimeEvent(time).to_json()
                await self.utility.send_message_raw(time_event, world_player.websocket)
            
            # sleep 10 minutes
            await asyncio.sleep(60 * 10)

    # just returns a specific room in our list of rooms
    async def get_room(self, room_id):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)         
        room = [room for room in self.rooms.get_rooms() if room.id == room_id][0]
        LogUtils.debug(f"{method_name}: exit, returning room \"{room.name}\"", self.logger)
        return room

    async def generate_map(self, player, environment = Environments.TOWNSMEE):
        self.path = f"c:/src/mud_images"
        image_name = f"{player.name}_map_{int(time.time())}".lower()
        extension = ".svg"
        full_path = f"{self.path}/{image_name}"
        full_tmp_path = f"{self.path}/tmp/{image_name}"
        
        # felete file if it exists
        if os.path.exists(image_name):
            os.remove(image_name)

        # get rooms
        rooms = [a for a in self.rooms.get_rooms() if a.environment == environment]
        
        # find area
        room = rooms[player.location_id]

        # generate map
        # graph_type="digraph",
        graph = pydot.Dot(
            player.name,
            graph_type="digraph",
            bgcolor="hotpink",
            rankdir="LR",
            splines="ortho",
            concentrate="true"
        )
        graph.set_node_defaults(
            shape="rectangle",
            style="filled",
            fillcolor="cornflowerblue",
            fontcolor="whitesmoke",
            fontname="monospace"
        )
        graph.set_edge_defaults(
            color="black",
            style="solid",
            dir="none",            
        )
        count = 0
        for room in rooms:
            count += 1
            print(f"Processing room: {room.name}, {count} of {len(rooms)}")
            room_name = room.name
            room_exits = room.exits
            for exit in room_exits:
                exit_room = rooms[exit["id"]]
                exit_direction = exit["direction"][0]
                edge = pydot.Edge(
                    room_name,
                    exit_room.name,
                    label=exit_direction,
                )
                graph.add_edge(edge)

        output_graphviz_svg = graph.create_svg()
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))
            
        
        with open(full_path + extension, "r") as text_file:
            main = text_file.read()
            main = re.sub('width=\"\d*pt\"', '', main)
            main = re.sub('height=\"\d*pt\"', '', main)
            
            # mini-map
            with open(f"{full_path}_mini{extension}", "w") as final_text_file:
                final_text_file.write(main)    
                
            # map map
            main = re.sub('viewbox=\".*\"', '', main)
            with open(full_path + extension, "w") as final_text_file:
                final_text_file.write(main)    
                                                 
        # send map event
        map_event = MapEvent(image_name).to_json()
        await self.utility.send_message_raw(map_event, player.websocket)
        