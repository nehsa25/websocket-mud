import asyncio
import inspect
import time
from aiimages import AIImages
from log_utils import LogUtils
from map import Map
from townsmee import TownSmee
from utility import Utility

class Environments(Utility):
    running_image_threads = []
    running_map_threads = []
    logger = None
    townsmee = None
    graveyard = None
    forest = None
    jungle = None
    breach = None
    beach = None
    all_rooms = []
    map = None 
    ai_images = None

    def __init__(self, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Environments() class", self.logger) 
        
        if self.ai_images is None:
            self.ai_images = AIImages(self.logger)

        if self.map is None:
            self.map = Map(self.logger)
        
        if self.townsmee is None:
            self.townsmee = TownSmee(self.logger)
            self.all_rooms.extend(self.townsmee.rooms)
        
        LogUtils.info(f"{method_name}: The world has {len(self.all_rooms)} rooms", self.logger)
            
    # returns the name of the area based on the type    
    def get_area_identifier(self, area):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        result = ""
        for env in Utility.Share.EnvironmentTypes:
            if area == env.name:
                result = env.name
        LogUtils.debug(f"{method_name}: exit, returning: {result}", self.logger)
        return result

    async def update_room(self, room, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)     
        for r in world.environments.rooms:
            if r.id == room.id:
                r = room
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return world.environments
    
    # returns player, world, responsible for moving a player from one room to the next
    async def move_room(self, new_room_id, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        # add player to new room
        new_room = await world.environments.get_room(new_room_id)
        new_room.players.append(player)

        # if the player has a previous room, update it        
        if player.room is not None:
            old_room = await world.environments.get_room(player.room.id)

            if old_room != new_room:
                for monster in old_room.monsters:
                    if monster.in_combat == player:
                        monster.in_combat = None

                # remove player from old room
                old_room.players.remove(player)
        
        # update to new room
        player.previous_room = player.room
        player.room = new_room
        
        # show new room
        player, world = await player.room.process_room(player, world)

        # name for images
        map_image_name = self.sanitize_filename(f"{player.name}_map_{int(time.time())}".lower()) # renkath_map_1718628698
        room_image_name = self.sanitize_filename(f"{new_room.name}_room_{int(time.time())}".lower()) + ".png" # townsquare_room_1718628698
        
        # generate new map (in a new task so we don't block the player)
        self.running_map_threads.append(asyncio.create_task(self.map.generate_map(new_room, map_image_name, player, world)))

        # generate a new room image (in a new task so we don't block the player)
        self.running_image_threads.append(asyncio.create_task(self.ai_images.generate_room_image(room_image_name, new_room.description, new_room.inside, player, world)))

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world

    # just returns a specific room in our list of rooms
    async def get_room(self, room_id):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, room_id: {room_id}", self.logger)
        room = [room for room in self.all_rooms if room.id == room_id][0]
        LogUtils.debug(
            f'{method_name}: exit, returning room "{room.name}"', self.logger
        )
        return room
