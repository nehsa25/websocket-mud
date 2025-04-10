from enum import Enum
import inspect
import os
import re
import pydot
from dontcheckin import DevSettings
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

        if ImageSize == Map.ImageSize.MINI:
            map_output = re.sub('width="\d*pt"', 'width="1200pt"', map_output)
            map_output = re.sub('height="\d*pt"', '', map_output)   
        elif ImageSize == Map.ImageSize.SMALL:
            map_output = re.sub('width="\d*pt"', 'width="1600pt"', map_output)
            map_output = re.sub('height="\d*pt"', '', map_output)
        else:
            map_output = re.sub('width="\d*pt"', '', map_output)
            map_output = re.sub('(viewBox="[^"]+")', '', map_output)  
            map_output = re.sub('height="\d*pt"', '', map_output)            
        map_output = re.sub(area_identifier + "\s&#45;\s", ": ", map_output)
        map_output = re.sub('&#45;\d*', "", map_output)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return map_output

    async def generate_map(self, room, image_name, player, world_state, area_identifier, environment=Utility.EnvironmentTypes.TOWNSMEE):
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
    
        self.path = f"{DevSettings.data_location}/mud-images"
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
            LogUtils.error(f"{method_name}: {e}", self.logger)
            return

        # write original to file
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))

        mini_image_url = None 

        # Upload different sizes to S3
        for size in [Map.ImageSize.MINI, Map.ImageSize.SMALL, Map.ImageSize.LARGE]:
            if size == Map.ImageSize.MINI:
                suffix = "_mini"
            elif size == Map.ImageSize.SMALL:
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

            if not image_url:
                LogUtils.error(f"{method_name}: Failed to upload {s3_key} to S3", self.logger)
            else:
                # Delete the temporary file
                os.remove(temp_image_path)
                if size == Map.ImageSize.MINI:
                    mini_image_url = image_url 

        # send map event
        map_event = MudEvents.MapEvent(mini_image_url)
        await self.send_message(map_event, player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)