from enum import Enum
import inspect
import os
import re
import pydot
from settings.exception import ExceptionUtils
from settings.settings import MudSettings
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility
import os
from utilities.aws import S3Utils

class Map(Utility):
    class ImageSize(Enum):
        MINI = 0
        SMALL = 1
        LARGE = 2
        
    logger = None
    def __init__(self, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: Initializing Map() class", logger)
        self.logger = logger

    async def sanitize_svg_output(self, map_output, area_identifier, ImageSize=ImageSize.LARGE):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        if ImageSize == Map.ImageSize.MINI or ImageSize == Map.ImageSize.SMALL:
            map_output = re.sub('width="\d*pt"', '', map_output)
            map_output = re.sub('height="\d*pt"', '', map_output)    
        map_output = re.sub(area_identifier + "\s&#45;\s", ": ", map_output)
        map_output = re.sub('&#45;\d*', "", map_output)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return map_output

    async def generate_full_map(self, room, image_name, player, world_state, area_identifier, environment=Utility.EnvironmentTypes.TOWNSMEE):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.graph = pydot.Dot(
            "mud_map",
            graph_type="digraph",
            bgcolor="#999",
            splines="ortho",
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
            style="dotted"
        )
    
        self.path = f"{MudSettings.data_location}/mud-images"
        extension = ".svg"
        full_path = f"{self.path}/{image_name}"

        # Ensure the directory exists
        os.makedirs(self.path, exist_ok=True)

        # delete file if it exists
        if os.path.exists(image_name):
            os.remove(image_name)

        # generate map
        count = 0
        for room in world_state.environments.rooms:
            count += 1
            room_name = room.name
            room_exits = room.exits
            
            # change color of active node
            active_node = False
            if room.name == player.room.name:
                active_node = True
                node = pydot.Node(room_name, fillcolor = "springgreen", fontcolor="black")
                self.graph.add_node(node)
            
            for exit in room_exits:
                exit_room = exit["id"]
                exit_direction = exit["direction"].name
                edge = pydot.Edge(room_name, exit_room.name, label=exit_direction)
                if active_node:
                    edge = pydot.Edge(room_name, 
                                      exit_room.name,
                                      label=exit_direction,
                                      style="line",
                                      fillcolor = "red")
                self.graph.add_edge(edge)

        try:
            output_graphviz_svg = self.graph.create_svg()
        except Exception as e:
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", self.logger)
            return

        # write original to file
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))

        # Upload different sizes to S3
        for size in [Map.ImageSize.SMALL, Map.ImageSize.LARGE]:
            if size == Map.ImageSize.SMALL:
                suffix = "_small"
            else:
                suffix = ""

            # Sanitize SVG output
            sanitized_svg = await self.sanitize_svg_output(output_graphviz_svg.decode("utf-8"), area_identifier, size)

            # Save sanitized SVG to a temporary file
            temp_image_path = f"{full_path}{suffix}{extension}"
            with open(temp_image_path, "w") as temp_file:
                temp_file.write(sanitized_svg)

            # Upload to S3
            s3_key = f"public/images/maps/{image_name}{suffix}{extension}"
            image_url = S3Utils.upload_image_to_s3(temp_image_path, s3_key)

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return image_url
    
    async def generate_mini_map(self, room, image_name, player, world_state, area_identifier, environment=Utility.EnvironmentTypes.TOWNSMEE):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.graph = pydot.Dot(
            "mud_map",
            graph_type="digraph",
            bgcolor="#999",
            splines="ortho",
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
            style="dotted"
        )
    
        self.path = f"{MudSettings.data_location}/mud-images"
        extension = ".svg"
        suffix = "_mini"
        full_path = f"{self.path}/{image_name}"

        # Ensure the directory exists
        os.makedirs(self.path, exist_ok=True)

        # delete file if it exists
        if os.path.exists(image_name):
            os.remove(image_name)

        # Helper function to recursively add rooms to the graph
        async def add_rooms_recursive(current_room, depth, active_room):
            if depth <= 0:
                return

            # change color of active node
            if current_room.name == active_room.name:
                node = pydot.Node(current_room.name, fillcolor = "springgreen", fontcolor="black")
                self.graph.add_node(node)
            else:
                node = pydot.Node(current_room.name)
                self.graph.add_node(node)

            for exit in current_room.exits:
                if exit != []:
                    exit_room = exit["id"]
                    exit_direction = exit["direction"].name

                    edge = pydot.Edge(current_room.name, exit_room.name, label=exit_direction)
                    self.graph.add_edge(edge)

                    await add_rooms_recursive(exit_room, depth - 1, active_room)

        # Start with the player's current room
        current_room = player.room
        await add_rooms_recursive(current_room, 2, current_room)

        try:
            output_graphviz_svg = self.graph.create_svg()
        except Exception as e:
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", self.logger)
            return

        # write original to file
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))

            # Sanitize SVG output
            sanitized_svg = await self.sanitize_svg_output(output_graphviz_svg.decode("utf-8"), area_identifier, Map.ImageSize.MINI)

            # Save sanitized SVG to a temporary file
            temp_image_path = f"{full_path}{suffix}{extension}"
            with open(temp_image_path, "w") as temp_file:
                temp_file.write(sanitized_svg)

            # Upload to S3
            s3_key = f"public/images/maps/{image_name}{suffix}{extension}"
            image_url = S3Utils.upload_image_to_s3(temp_image_path, s3_key)

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return image_url
    
    async def generate_map(self, room, image_name, player, world_state, area_identifier, environment=Utility.EnvironmentTypes.TOWNSMEE):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # generate full map
        full_map_url = await self.generate_full_map(room, image_name, player, world_state, area_identifier, environment)

        # generate mini map
        mini_map_url = await self.generate_mini_map(room, image_name, player, world_state, area_identifier, environment)

        # send map event
        map_event = MudEvents.MapEvent(full_map_url, mini_map_url)
        await self.send_message(map_event, player.websocket)