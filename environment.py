from copy import deepcopy
import inspect
import time
from directions.direction import Directions
from environments.townsmee import TownSmee
from log_utils import LogUtils
from monster import Monster
from npc import Npc
from room import Room
from utility import Utility


class Environments(Utility):
    class RoomHistory:
        room_id: int = None
        player_name: str
        message: str
        creation_time = None
        response_time = None
        players_in_room = []
        npcs_in_room = []
        monsters_in_room = []
        
        def __init__(self, room_id, player_name, message, world_state):
            self.room_id = room_id
            self.player_name = player_name
            self.message = message            
            room = world_state.get_room(room_id)
            self.players_in_room = room.players
            self.npcs_in_room = room.npcs
            self.monsters_in_room = room.monsters
            self.creation_time = time.time()
            
    class Rooms(Utility): 
        environment = None

        def __init__(self, logger) -> None:
            self.logger = logger
            LogUtils.debug(f"Initializing Environments.Rooms() class", self.logger)

        def add_room(
            self,
            id,
            name,
            inside,
            description,
            exits,
            environment,
            scariness,
            in_town=False,
            items=[],
            hidden_items=[],
            monsters=[],
            players=[],
            npcs=[],
        ):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            room = Room(
                id=id,
                name=name,
                inside=inside,
                description=description,
                exits=exits,
                environment=environment,
                scariness=scariness,
                items=items,
                in_town=in_town,
                hidden_items=hidden_items,
                monsters=monsters,
                players=players,
                npcs=npcs,
                logger=self.logger
            )
            LogUtils.debug(f"{method_name}: generated room: {room}", self.logger)
            return room
    
    npcs = None
    monster = None
    running_image_threads = []
    running_map_threads = []
    logger = None
    townsmee = None
    all_rooms = []
    all_npcs = []
    dirs = None
    room_history = []

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Environments() class", self.logger)

        self.dirs = Directions(self.logger)

        if self.npcs is None:
            self.npcs = Npc(self.logger)

        if self.monster is None:
            self.monster = Monster(self.logger)

        if self.townsmee is None:
            self.townsmee = TownSmee(self.dirs, self.logger)
            self.all_rooms.extend(self.townsmee.rooms)

        # add in npcs
        LogUtils.info(
            f"{method_name}: The world has {len(self.all_rooms)} rooms", self.logger
        )

    async def update_room_history(self, room_id, player_name, message, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        room_histories = []
        histories = deepcopy(self.room_history)
        last_history = None
        for history in histories:
            if room_id == history.room_id:
                last_history.response_time = time.time()
                room_histories.append(last_history)
            else:
                room_histories.append(self.append_room_history(room_id, player_name, message, world_state))

        room_histories.append(history)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        self.room_history = deepcopy(room_histories)
        
    async def append_room_history(self, room_id, player_name, message, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, message: {message}", self.logger)
        room_history_message = self.RoomHistory(room_id, player_name, message, world_state)
        self.room_history.append(room_history_message)
        LogUtils.debug(f"{method_name}: exit", self.logger)  
        
    async def get_room_history(self, room_id):
        lines = [a for a in self.room_history if a.id == room_id]
        return lines
