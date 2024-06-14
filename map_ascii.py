import pydot

import traceback
import logging
import math
import os
import pydoc
import sys
from log_utils import Level, LogUtils
from townsmee import TownSmee

class AsciiArt:    
    logger = None

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing AsciiArt() class", self.logger)
            
    def pydot(self, rooms):
        graph = pydot.Dot("Town Smee", graph_type='digraph',rankdir="LR", bgcolor="yellow", style="dotted")
        graph.set_node_defaults(shape="rectangle", style="filled", fillcolor="lightblue", fontsize="16", fontcolor="black", color="black", fontname="monospace")
        for room in rooms:
            room_id = room.id
            room_name = room.name
            room_exits = room.exits
            for exit in room_exits:
                exit_room = rooms[exit['id']]
                exit_direction = exit['direction'][0]
                exit_id = exit_room.id
                edge = pydot.Edge(room_name, exit_room.name, label=exit_direction, color="black", fontsize="16", style="dotted", fontname="monospace", simplify=True)
                graph.add_edge(edge)
                

        graph.write_png("output.png")
        
        # # Add nodes
        # my_node = pydot.Node("a", label=name)
        # graph.add_node(my_node)
        # # Or, without using an intermediate variable:
        # graph.add_node(pydot.Node("b", shape="circle"))

        # # Add edges
        # my_edge = pydot.Edge("a", "b", color="blue")
        # graph.add_edge(my_edge)
        # # Or, without using an intermediate variable:
        # graph.add_edge(pydot.Edge("b", "c", color="blue"))
        # graph.write_png("output.png")
        
    def surrund_room(self, room_name):
        LogUtils.debug("surround_room() enter", self.logger)
        top = "v" * int(len(room_name) + 2)
        bottom = "v" * int(len(room_name) + 2)
        leftright = "|"
        room = f"{top}\n{leftright}{room_name}{leftright}\n{bottom}"
        LogUtils.debug("surround_room() exit", self.logger)
        return room
        
    def rooma_below_roomb(self, rooma, roomb):
        LogUtils.debug("rooma_below_roomb() enter", self.logger)
        room_half = len(rooma)/2-1
        room_sep = " " * int(room_half)
        if rooma < roomb:
            rooma = " " * (len(roomb) - len(rooma)) + rooma
        if roomb < rooma:
            roomb = roomb + " " * (len(rooma) - len(roomb))
            
        ascii_rooma = self.surrund_room(rooma)
        ascii_roomb = self.surrund_room(roomb)
        
        room = f"{ascii_rooma}\n{room_sep}|{room_sep}\n{ascii_roomb}"
        LogUtils.debug("rooma_below_roomb() exit", self.logger)
        return room
    
    def rooma_above_roomb(self, rooma, roomb):
        LogUtils.debug("rooma_above_roomb() enter", self.logger)
        room_half = len(rooma)/2-1
        room_sep = " " * int(room_half)
        ascii_rooma = self.surrund_room(rooma)
        ascii_roomb = self.surrund_room(roomb)
        room = f"{ascii_roomb}\n{room_sep}|{room_sep}\n{ascii_rooma}"
        LogUtils.debug("rooma_above_roomb() exit", self.logger)
        return room
        

if __name__ == "__main__":
    try:
        # setup logger
        logger = LogUtils.get_logger(
            filename="map_ascii.log",
            file_level=Level.DEBUG,
            console_level=Level.INFO,
            log_location="c:\\src\\websocket-mud",
        )
        
        townsmee = TownSmee(logger)
        a = AsciiArt(logger)
        a.pydot(townsmee.rooms)
            
        
        # a = AsciiArt(logger)
        
        # # test class - eventually will be called from world.py
        # townsmee = TownSmee(logger)
        
        # for room in townsmee.rooms:
        #     print(f"\n\n\nProcess Room: {room.name}")
        #     for dir in room.exits:
        #         direction = dir['direction'][0]
        #         room_id = dir['id']
        #         dir_room_name = townsmee.rooms[room_id].name
        #         if direction == 'd':
        #             print(a.rooma_below_roomb(room.name, dir_room_name))    
        #         elif direction == 'u':
        #             print(a.rooma_above_roomb(room.name, dir_room_name))     
    except:
        print(f"An error occurred!\nException:\n{traceback.format_exc()}")
