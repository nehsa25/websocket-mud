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
        LogUtils.debug(f"{method_name}: enter with area_identifier: {area_identifier} and ImageSize: {ImageSize}", self.logger)

        if ImageSize == Map.ImageSize.MINI or ImageSize == Map.ImageSize.SMALL:
            map_output = re.sub('width="\d*pt"', '', map_output)
            map_output = re.sub('height="\d*pt"', '', map_output)    
        map_output = re.sub(area_identifier + "\s&#45;\s", ": ", map_output)
        map_output = re.sub('&#45;\d*', "", map_output)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return map_output
    
    async def _generate_map(self, room, image_name, player, world_state, area_identifier, is_mini=False):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter with image_name: {image_name}, area_identifier: {area_identifier}, is_mini: {is_mini}", self.logger)

        mini_map_room_depth = 3

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
        suffix = "_mini" if is_mini else ""
        full_path = f"{self.path}/{image_name}"

        # Ensure the directory exists
        LogUtils.debug(f"{method_name}: Creating directories for: {self.path}", self.logger)
        os.makedirs(self.path, exist_ok=True)

        # delete file if it exists
        if os.path.exists(image_name):
            LogUtils.debug(f"{method_name}: Deleting filename: {image_name}", self.logger)
            os.remove(image_name)

        if is_mini:
            async def add_rooms_recursive(current_room, depth, active_room, visited_rooms=None):
                if visited_rooms is None:
                    visited_rooms = set()

                LogUtils.debug(f"{method_name}: add_rooms_recursive depth: {depth}, active_room name: {active_room.name}, current_room name: {current_room.name}, visited_rooms: {len(visited_rooms)}", self.logger)

                if depth <= 0 or current_room in visited_rooms:
                    LogUtils.debug(f"{method_name}: add_rooms_recursive returning early, depth: {depth}, current_room: {current_room.name if current_room else 'None'} in visited_rooms: {current_room in visited_rooms if current_room else 'N/A'}", self.logger)
                    return

                visited_rooms.add(current_room)

                # change color of active node
                if current_room.name == active_room.name:
                    node = pydot.Node(current_room.name, fillcolor = "springgreen", fontcolor="black")
                    self.graph.add_node(node)
                    LogUtils.debug(f"{method_name}: add_rooms_recursive added active node: {current_room.name}", self.logger)
                else:
                    node = pydot.Node(current_room.name)
                    self.graph.add_node(node)
                    LogUtils.debug(f"{method_name}: add_rooms_recursive added node: {current_room.name}", self.logger)

                LogUtils.debug(f"{method_name}: add_rooms_recursive current_room.exits: {current_room.exits}", self.logger)
                for exit in current_room.exits:
                    LogUtils.debug(f"{method_name}: add_rooms_recursive processing exit: {exit}", self.logger)
                    if exit != []:
                        exit_room = exit["id"]
                        exit_direction = exit["direction"].name

                        edge = pydot.Edge(current_room.name, exit_room.name, label=exit_direction)
                        self.graph.add_edge(edge)
                        LogUtils.debug(f"{method_name}: add_rooms_recursive added edge from: {current_room.name} to {exit_room.name} with label: {exit_direction}", self.logger)

                        await add_rooms_recursive(exit_room, depth - 1, active_room, visited_rooms)
                    else:
                        LogUtils.debug(f"{method_name}: add_rooms_recursive exit is empty", self.logger)
            # Start with the player's current room
            current_room = player.room
            LogUtils.debug(f"{method_name}: add_rooms_recursive starting with current_room: {current_room.name}", self.logger)
            await add_rooms_recursive(current_room, 1, current_room)
        else:
            # generate map
            for room in world_state.environments.rooms:
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
            return None

        # write original to file
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))

        image_size = Map.ImageSize.MINI if is_mini else Map.ImageSize.SMALL
        # Sanitize SVG output
        sanitized_svg = await self.sanitize_svg_output(output_graphviz_svg.decode("utf-8"), area_identifier, image_size)

        # Save sanitized SVG to a temporary file
        temp_image_path = f"{full_path}{suffix}{extension}"
        with open(temp_image_path, "w") as temp_file:
            result = temp_file.write(sanitized_svg)
            if result == None or result == 0:
                LogUtils.error(f"{method_name}: Error writing to file: {temp_image_path}", self.logger)
                return None

        # Upload to S3
        s3_key = f"public/images/maps/{image_name}{suffix}{extension}"
        LogUtils.debug(f"{method_name}: Uploading to S3 with key: {s3_key}", self.logger)
        S3Utils.upload_image_to_s3(temp_image_path, 
                                    s3_key, 
                                    make_public=True, 
                                    content_type='image/svg+xml', 
                                    logger=self.logger)
        
        image_url = S3Utils.generate_public_url(s3_key)
        LogUtils.debug(f"{method_name}: Image URL from S3: {image_url}", self.logger)

        LogUtils.debug(f"{method_name}", self.logger)
        return image_url

    async def generate_full_map(self, room, image_name, player, world_state, area_identifier, environment=Utility.EnvironmentTypes.TOWNSMEE):
        LogUtils.debug(f"generate_full_map: enter with image_name: {image_name}, area_identifier: {area_identifier}", self.logger)
        result = await self._generate_map(room, image_name, player, world_state, area_identifier, is_mini=False)
        LogUtils.debug(f"generate_full_map: exit with result: {result}", self.logger)
        return result
    
    async def generate_mini_map(self, room, image_name, player, world_state, area_identifier, environment=Utility.EnvironmentTypes.TOWNSMEE):
        LogUtils.debug(f"generate_mini_map: enter with image_name: {image_name}, area_identifier: {area_identifier}", self.logger)
        result =  await self._generate_map(room, image_name, player, world_state, area_identifier, is_mini=True)
        LogUtils.debug(f"generate_mini_map: exit with result: {result}", self.logger)
        return result
    
    async def generate_map(self, room, image_name, player, world_state, area_identifier, environment=Utility.EnvironmentTypes.TOWNSMEE):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter with image_name: {image_name}, area_identifier: {area_identifier}", self.logger)

        # generate full map
        full_map_url = await self.generate_full_map(room, image_name, player, world_state, area_identifier, environment)
        LogUtils.debug(f"{method_name}: Full map URL: {full_map_url}", self.logger)

        # generate mini map
        mini_map_url = await self.generate_mini_map(room, image_name, player, world_state, area_identifier, environment)
        LogUtils.debug(f"{method_name}: Mini map URL: {mini_map_url}", self.logger)

        # send map event
        map_event = MudEvents.MapEvent(full_map_url, mini_map_url)
        await self.send_message(map_event, player.websocket)