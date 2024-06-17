import inspect
from threading import Thread
import time
from aiimages import AIImages
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility
from townsmee import TownSmee

# from breach import Breach
# from forest import Forest
# from jungle import Jungle


class Rooms(Utility):
    logger = None
    # forest = Forest()
    # breach = Breach()
    # jungle = Jungle()
    townsmee = None
    envionments = []
    world_name = ""
    rooms = []

    def __init__(self, world_name, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Rooms() class", self.logger)

        self.world_name = world_name
        if self.townsmee is None:
            self.townsmee = TownSmee(self.world_name, self.logger)
            self.envionments.append(self.townsmee)

        # self.all_rooms.extend(self.forest.rooms)
        # self.all_rooms.extend(self.breach.rooms)
        # self.all_rooms.extend(self.jungle.rooms)

        # build our room list
        for env in self.envionments:
            self.rooms.extend(env.rooms)

        LogUtils.info(f"{self.world_name}  has {len(self.rooms)} rooms", self.logger)

    # returns the name of the area based on the type
    def get_area_identifier(self, area):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        result = ""
        for env in self.envionments:
            if area == env.type:
                result = env.name
        LogUtils.debug(f"{method_name}: exit, returning: {result}", self.logger)
        return result

    # returns player, world, responsible for moving a player from one room to the next
    async def move_room(self, new_room_id, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        old_room = await world.rooms.get_room(player.location_id)
        new_room = await world.rooms.get_room(new_room_id)

        if old_room != new_room:
            for monster in old_room.monsters:
                if monster.in_combat == player:
                    monster.in_combat = None

            # remove player from old room
            old_room.players.remove(player)

        # add player to new room
        new_room.players.append(player)
        player.location_id = new_room.id

        # show new room
        player, world = await self.process_room(new_room_id, player, world)

        # name for images
        map_image_name = self.sanitize_filename(f"{player.name}_map_{int(time.time())}".lower()) # renkath_map_1718628698
        room_image_name = f"{self.sanitize_filename(new_room.name)}.png"
        
        # generate new map (in a new task so we don't block the player)
        map_thread = Thread(target = world.map.start_async, args = (new_room, map_image_name, player, world))
        map_thread.start()

        # generate a new room image (in a new task so we don't block the player)
        # room_image_thread = Thread(target = world.ai_images.start_async, args = (room_image_name, new_room.description, player))
        # room_image_thread.start()
        
        # map_thread.join()
        # room_image_thread.join()
        
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world

    # returns player, world
    async def process_room(self, new_room_id, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        new_room = await self.get_room(new_room_id)

        # get the description
        description = new_room.description

        # show items
        items = ""
        if len(new_room.items) > 0:
            for item in new_room.items:
                items += item.name + ", "
            items = items[0 : len(items) - 2]

        # offer possible exits
        exits = ""
        for available_exit in new_room.exits:
            exits += available_exit["direction"][1] + ", "
        exits = exits[0 : len(exits) - 2]

        # show monsters
        monsters = ""
        for monster in new_room.monsters:
            monsters += monster.name + ", "
        monsters = monsters[0 : len(monsters) - 2]

        # show people
        people = ""
        for p in world.players.players:
            if player.name == p.name:
                continue
            if p.location_id == new_room_id:
                people += p.name + ", "
        if people != "":
            people = people[0 : len(people) - 2]

        # formulate message to client
        json_msg = MudEvents.RoomEvent(
            new_room.name, description, items, exits, monsters, people
        ).to_json()

        LogUtils.debug(f"Sending json: {json_msg}", self.logger)
        await self.send_message(json_msg, player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world

    # just returns a specific room in our list of rooms
    async def get_room(self, room_id):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, room_id: {room_id}", self.logger)
        room = [room for room in self.rooms if room.id == room_id][0]
        LogUtils.debug(
            f'{method_name}: exit, returning room "{room.name}"', self.logger
        )
        return room
