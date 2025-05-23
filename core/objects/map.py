import os
import re
import pydot
from core.enums.image_size import ImageSizeEnum
from core.events.map import MapEvent
from utilities.exception import ExceptionUtility
from settings.global_settings import GlobalSettings
from utilities.log_telemetry import LogTelemetryUtility
from utilities.aws import AWSUtility


class Map:
    logger = None

    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Map() class")

    async def sanitize_svg_output(self, map_output, area_identifier, ImageSize=ImageSizeEnum.LARGE):
        self.logger.debug(f"enter with area_identifier: {area_identifier} and ImageSize: {ImageSize}")

        if ImageSize == ImageSize.MINI or ImageSize == ImageSize.SMALL:
            map_output = re.sub('width="\\d*pt"', "", map_output)
            map_output = re.sub('height="\\d*pt"', "", map_output)
        map_output = re.sub(area_identifier + r"\s&#45;\s", ": ", map_output)
        map_output = re.sub("&#45;\\d*", "", map_output)
        self.logger.debug("exit")
        return map_output

    async def _generate_map(self, room, image_name, player, area_identifier, is_mini=False):
        self.logger.debug(
            f"enter with image_name: {image_name}, area_identifier: {area_identifier}, is_mini: {is_mini}"
        )
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

        self.graph.set_edge_defaults(color="black", style="dotted")

        self.path = f"{GlobalSettings.DATA_LOCATION}/mud-images"
        extension = ".svg"
        suffix = "_mini" if is_mini else ""
        full_path = f"{self.path}/{image_name}"

        # Ensure the directory exists
        self.logger.debug(f"Creating directories for: {self.path}")
        os.makedirs(self.path, exist_ok=True)

        # delete file if it exists
        if os.path.exists(image_name):
            self.logger.debug(f"Deleting filename: {image_name}")
            os.remove(image_name)

        if is_mini:

            async def add_rooms_recursive(current_room, depth, active_room, visited_rooms=None):
                if visited_rooms is None:
                    visited_rooms = set()

                self.logger.debug(
                    f"add_rooms_recursive depth: {depth}, active_room name: {active_room.name}, current_room name: {current_room.name}, visited_rooms: {len(visited_rooms)}"
                )

                if depth <= 0 or current_room in visited_rooms:
                    self.logger.debug(
                        f"add_rooms_recursive returning early, depth: {depth}, current_room: {current_room.name if current_room else 'None'} in visited_rooms: {current_room in visited_rooms if current_room else 'N/A'}"
                    )
                    return

                visited_rooms.add(current_room)

                # change color of active node
                if current_room.name == active_room.name:
                    node = pydot.Node(current_room.name, fillcolor="springgreen", fontcolor="black")
                    self.graph.add_node(node)
                    self.logger.debug(f"add_rooms_recursive added active node: {current_room.name}")
                else:
                    node = pydot.Node(current_room.name)
                    self.graph.add_node(node)
                    self.logger.debug(f"add_rooms_recursive added node: {current_room.name}")

                self.logger.debug(f"add_rooms_recursive current_room.exits: {current_room.exits}")
                for exit in current_room.exits:
                    self.logger.debug(f"add_rooms_recursive processing exit: {exit}")
                    if exit != []:
                        exit_room = exit["id"]
                        exit_direction = exit["direction"].name

                        edge = pydot.Edge(current_room.name, exit_room.name, label=exit_direction)
                        self.graph.add_edge(edge)
                        self.logger.debug(
                            f"add_rooms_recursive added edge from: {current_room.name} to {exit_room.name} with label: {exit_direction}"
                        )

                        await add_rooms_recursive(exit_room, depth - 1, active_room, visited_rooms)
                    else:
                        self.logger.debug("add_rooms_recursive exit is empty")

            # Start with the player's current room
            current_room = player.room
            self.logger.debug(f"add_rooms_recursive starting with current_room: {current_room.name}")
            await add_rooms_recursive(current_room, 1, current_room)
        else:
            # generate map
            for room in self.world_service.environments.rooms:
                room_name = room.name
                room_exits = room.exits

                # change color of active node
                active_node = False
                if room.name == player.room.name:
                    active_node = True
                    node = pydot.Node(room_name, fillcolor="springgreen", fontcolor="black")
                    self.graph.add_node(node)

                for exit in room_exits:
                    exit_room = exit["id"]
                    exit_direction = exit["direction"].name
                    edge = pydot.Edge(room_name, exit_room.name, label=exit_direction)
                    if active_node:
                        edge = pydot.Edge(
                            room_name,
                            exit_room.name,
                            label=exit_direction,
                            style="line",
                            fillcolor="red",
                        )
                    self.graph.add_edge(edge)

        try:
            output_graphviz_svg = self.graph.create_svg()
        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")
            return None

        # write original to file
        with open(full_path + extension, "w") as text_file:
            text_file.write(output_graphviz_svg.decode("utf-8"))

        image_size = ImageSizeEnum.MINI if is_mini else ImageSizeEnum.SMALL
        # Sanitize SVG output
        sanitized_svg = await self.sanitize_svg_output(output_graphviz_svg.decode("utf-8"), area_identifier, image_size)

        # Save sanitized SVG to a temporary file
        temp_image_path = f"{full_path}{suffix}{extension}"
        with open(temp_image_path, "w") as temp_file:
            result = temp_file.write(sanitized_svg)
            if result is None or result == 0:
                self.logger.error(f"Error writing to file: {temp_image_path}")
                return None

        # Upload to S3
        s3_key = f"public/images/maps/{image_name}{suffix}{extension}"
        self.logger.debug(f"Uploading to S3 with key: {s3_key}")
        AWSUtility.upload_image_to_s3(
            temp_image_path,
            s3_key,
            make_public=True,
            content_type="image/svg+xml",
            logger=self.logger,
        )

        image_url = AWSUtility.generate_public_url(s3_key)
        self.logger.debug(f"Image URL from S3: {image_url}")
        return image_url

    async def generate_full_map(self, room, image_name, player, area_identifier):
        self.logger.debug(f"generate_full_map: enter with image_name: {image_name}, area_identifier: {area_identifier}")
        result = await self._generate_map(room, image_name, player, area_identifier, is_mini=False)
        self.logger.debug(f"generate_full_map: exit with result: {result}")
        return result

    async def generate_mini_map(self, room, image_name, player, area_identifier):
        self.logger.debug(f"generate_mini_map: enter with image_name: {image_name}, area_identifier: {area_identifier}")
        result = await self._generate_map(room, image_name, player, area_identifier, is_mini=True)
        self.logger.debug(f"generate_mini_map: exit with result: {result}")
        return result

    async def generate_map(self, room, image_name, player, area_identifier):
        self.logger.debug(f"enter with image_name: {image_name}, area_identifier: {area_identifier}")

        # generate full map
        full_map_url = await self.generate_full_map(room, image_name, player, area_identifier)
        self.logger.debug(f"Full map URL: {full_map_url}")

        # generate mini map
        mini_map_url = await self.generate_mini_map(room, image_name, player, area_identifier)
        self.logger.debug(f"Mini map URL: {mini_map_url}")

        # send map event
        await MapEvent(full_map_url, mini_map_url).send(player.websocket)
