import time
import pydot
import inspect
from items import Items
from log_utils import LogUtils
from mudevent import HealthEvent, InventoryEvent, MapEvent
from rooms import Rooms
from utility import Utility
import os

class Player:
    logger = None
    utility = None
    name = None
    rooms = None
    level = 1
    hitpoints = 0
    max_hitpoints = 0
    location = 0
    strength = 0
    agility = 0
    perception = 0
    experience = 0
    resting = False
    in_combat = None
    ip = None
    inventory = [Items.book, Items.cloth_pants]
    money = []
    websocket = None
    image_name = ""
    
    def __init__(
        self, name, hp, strength, agility, location, perception, ip, websocket, logger
    ):
        self.logger = logger
        LogUtils.debug(f"Initializing Player() class", self.logger)
        self.rooms = Rooms(logger)
        self.utility = Utility(logger)
        self.name = name
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.location = location
        self.ip = ip
        self.websocket = websocket

    # shows color-coded health bar
    async def show_health(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        msg = f"{self.name}|{str(self.hitpoints)}/{str(self.max_hitpoints)}"
        if self.resting:
            msg += "|REST"
        health_event = HealthEvent(msg).to_json()
        await self.utility.send_message_raw(health_event, self.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # shows inventory
    async def show_inventory(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        items = []
        for item in self.inventory:
            items.append(item.name)
        inv_event = InventoryEvent(items).to_json()
        await self.utility.send_message_raw(inv_event, self.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def generate_map(self, location):
        self.path = f"c:/src/mud_images"
        self.image_name = f"{self.name}_map_{int(time.time())}.png".lower()
        self.full_path = f"{self.path}/{self.image_name}"
        # felete file if it exists
        if os.path.exists(self.image_name):
            os.remove(self.image_name)

        # find area
        room = self.rooms.all_rooms[location]

        # generate map
        graph = pydot.Dot(
            self.name,
            graph_type="digraph",
            rankdir="LR",
            bgcolor="yellow",
            style="dotted",
        )
        graph.set_node_defaults(
            shape="rectangle",
            style="filled",
            fillcolor="lightblue",
            fontsize="16",
            fontcolor="black",
            color="black",
            fontname="monospace",
        )
        for room in self.rooms.all_rooms:
            room_name = room.name
            room_exits = room.exits
            for exit in room_exits:
                exit_room = self.rooms.all_rooms[exit["id"]]
                exit_direction = exit["direction"][0]
                edge = pydot.Edge(
                    room_name,
                    exit_room.name,
                    label=exit_direction,
                    color="black",
                    fontsize="16",
                    style="dotted",
                    fontname="monospace",
                    simplify=True,
                )
                graph.add_edge(edge)
        graph.write_png(self.full_path)
        
        # send map event
        map_event = MapEvent(self.image_name).to_json()
        await self.utility.send_message_raw(map_event, self.websocket)
        
