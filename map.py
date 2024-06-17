import asyncio
import base64
from enum import Enum
import inspect
import os
import re
import pydot
import requests
from environments import Environments
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility
import os

class Map(Utility):
    class ImageSize(Enum):
        MINI = 0
        SMALL = 1
        LARGE = 2
        
    logger = None
    def __init__(self, logger) -> None:
        LogUtils.debug("Initializing Map() class", logger)
        self.logger = logger

    def start_async(self, room, image_name, player, world, environment=Environments.TOWNSMEE):
        start_server = self.generate_map(room, image_name, player, world, environment)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(start_server)

    async def sanitize_svg_output(self, map_output, environment_name, world, ImageSize=ImageSize.LARGE):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        area_identifier = world.rooms.get_area_identifier(environment_name)
        if ImageSize == ImageSize.MINI:
            map_output = re.sub('width="\d*pt"', 'width="200pt"', map_output)
            map_output = re.sub('height="\d*pt"', '', map_output)   
        elif ImageSize == ImageSize.SMALL:
            map_output = re.sub('width="\d*pt"', 'width="800pt"', map_output)
            map_output = re.sub('height="\d*pt"', '', map_output)
        else:
            map_output = re.sub('width="\d*pt"', 'width="1200pt"', map_output)
            map_output = re.sub('height="\d*pt"', '', map_output)            
        map_output = re.sub(area_identifier + "\s&#45;\s", "", map_output)
        map_output = re.sub('&#45;\d*', "", map_output)
        LogUtils.debug(f"{method_name}: exit, returning: {map_output}", self.logger)
        return map_output

    async def generate_map(self, room, image_name, player, world, environment=Environments.TOWNSMEE):
        self.graph = pydot.Dot(
            "mud_map",
            graph_type="digraph",
            bgcolor="#999",
            splines="ortho",
            concentrate="true",
        )

        self.graph.set_node_defaults(
            shape="record",
            style="filled",
            fillcolor="cornflowerblue",
            fontcolor="whitesmoke",
            fontname="monospace",
        )

        self.graph.set_edge_defaults(
            color="black",
            style="dotted",
            dir="both",
        )
    
        self.path = f"c:/src/mud_images"
        extension = ".svg"
        full_path = f"{self.path}/{image_name}"

        # felete file if it exists
        if os.path.exists(image_name):
            os.remove(image_name)

        # get rooms
        rooms = [a for a in world.rooms.rooms if a.environment == environment]
 
        # generate map
        count = 0
        for room in rooms:
            count += 1
            print(f"Processing room: {room.name}, {count} of {len(rooms)}")
            room_name = room.name
            room_exits = room.exits
            
            # change color of active node
            active_node = False
            if room.id == player.location_id:
                active_node = True
                node = pydot.Node(room_name, fillcolor = "springgreen", fontcolor="black")
                self.graph.add_node(node)
            
            for exit in room_exits:
                exit_room = rooms[exit["id"]]
                exit_direction = exit["direction"][0]
                edge = pydot.Edge(room_name, exit_room.name, label=exit_direction)
                if active_node:
                    edge = pydot.Edge(room_name, 
                                      exit_room.name,
                                      label=exit["direction"][1],
                                      fillcolor = "red")
                self.graph.add_edge(edge)

        output_graphviz_svg = self.graph.create_svg()

        # write original to file
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))

        # clean it up
        with open(full_path + extension, "r") as text_file:
            contents = text_file.read()
            

            # mini-map
            with open(f"{full_path}_mini{extension}", "w") as final_text_file:
                main = await self.sanitize_svg_output(contents, environment, world, Map.ImageSize.MINI)
                final_text_file.write(main)
                
            # small
            with open(f"{full_path}_small{extension}", "w") as final_text_file:
                main = await self.sanitize_svg_output(contents, environment, world, Map.ImageSize.SMALL)
                final_text_file.write(main)
                                      
            # map
            with open(f"{full_path}{extension}", "w") as final_text_file:
                main = await self.sanitize_svg_output(contents, environment, world, Map.ImageSize.LARGE)
                final_text_file.write(main)              

        # send map event
        map_event = MudEvents.MapEvent(image_name)
        await self.send_message(map_event, player.websocket)