import inspect
import os
import re
import time
import pydot
from environments import Environments
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility


class Map(Utility):
    logger = None
    rooms = None
    graph = None

    def __init__(self, rooms, logger) -> None:
        LogUtils.debug("Initializing Map() class", logger)
        self.logger = logger
        self.rooms = rooms
        self.graph = pydot.Dot(
            "mud_map",
            graph_type="digraph",
            bgcolor="#999",
            rankdir="LR",
            splines="ortho",
            concentrate="true",
        )

        self.graph.set_node_defaults(
            shape="rectangle",
            style="filled",
            fillcolor="cornflowerblue",
            fontcolor="whitesmoke",
            fontname="monospace",
        )

        self.graph.set_edge_defaults(
            color="black",
            style="solid",
            dir="both",
        )

    async def santizie_svg_map_output(self, map_output, environment_name):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        area_identifier = await self.rooms.get_area_identifier(environment_name)
        map_output = re.sub('width="\d*pt"', "", map_output)
        map_output = re.sub('height="\d*pt"', "", map_output)
        map_output = re.sub(area_identifier + "\s&#45;\s", "", map_output)
        LogUtils.debug(f"{method_name}: exit, returning: {map_output}", self.logger)
        return map_output

    async def generate_map(self, player, world, environment=Environments.TOWNSMEE):
        self.path = f"c:/src/mud_images"
        image_name = f"{player.name}_map_{int(time.time())}".lower()
        extension = ".svg"
        full_path = f"{self.path}/{image_name}"

        # felete file if it exists
        if os.path.exists(image_name):
            os.remove(image_name)

        # get rooms
        rooms = [a for a in world.rooms.rooms if a.environment == environment]

        # find area
        room = rooms[player.location_id]

        # generate map
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
                self.graph.add_edge(edge)

        output_graphviz_svg = self.graph.create_svg()

        # write original to file
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))

        # clean it up
        with open(full_path + extension, "r") as text_file:
            main = await self.santizie_svg_map_output(text_file.read(), environment)

            # map
            with open(f"{full_path}{extension}", "w") as final_text_file:
                final_text_file.write(main)

        # send map event
        map_event = MudEvents.MapEvent(image_name).to_json()
        await self.send_message(map_event, player.websocket)
