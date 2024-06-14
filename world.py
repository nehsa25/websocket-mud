import asyncio
import datetime
import inspect
from random import randint
from mudevent import TimeEvent
from rooms import Rooms
from utility import Utility
from log_utils import LogUtils, Level
from command import Command

class World:
    # players
    players = []
    breeze_task = None
    rain_task = None
    eerie_task = None
    thunder_task = None
    mob_attack_task = None
    time_task = None
    logger = None
    utility = None
    command = None
    rooms = None
    rooms_list = None
    
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing World() class", self.logger)
        self.utility = Utility(self.logger)
        self.command = Command(self.logger)
        self.rooms = Rooms(self.logger)
        self.rooms_list = self.rooms.all_rooms

    # schedule some events that'll do shit
    async def setup_world_events(self):        
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        if self.breeze_task == None:
            self.breeze_task = asyncio.create_task(self.breeze())
            
        if self.rain_task == None:
            self.rain_task = asyncio.create_task(self.rain())

        if self.eerie_task == None:
            self.eerie_task = asyncio.create_task(self.eerie_silence())

        if self.thunder_task == None:
            self.thunder_task = asyncio.create_task(self.thunder())

        if self.time_task == None:
            self.time_task = asyncio.create_task(self.get_system_time())

    # It begins to rain..
    async def rain(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 3600*2)
            LogUtils.debug(f"Will run rain1 event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("It begins to rain..", 'event', world_player.websocket)

            # wait for it to stop
            rand = randint(100, 500)
            LogUtils.debug(f"Will run rain2 event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("The rain pitter-patters to a stop and the sun begins to shine through the clouds..", 'event', world_player.websocket)

    # You hear thunder off in the distane..
    async def thunder(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 3800*2)
            LogUtils.debug(f"Will run thunder event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("You hear thunder off in the distance..", 'event', world_player.websocket)

    # A gentle breeze blows by you..
    async def breeze(self):    
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 3800*2)
            LogUtils.debug(f"Will run breeze event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("A gentle breeze blows by you..", 'event', world_player.websocket)

    # An eerie silence settles on the room..
    async def eerie_silence(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            rand = randint(2000, 4000*2)
            LogUtils.debug(f"Will run eerie_silence event in {str(rand)} seconds...", self.logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await self.utility.send_msg("An eerie silence settles on the room..", 'event', world_player.websocket)

    # responsible for moving a player from one room to the next
    async def move_room(self, new_room_id, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        old_room = await self.get_room(player.location)
        new_room = await self.get_room(new_room_id)

        if old_room != new_room:
            for monster in old_room.monsters:
                if monster.in_combat == player:
                    monster.in_combat = None

            # remove player from old room
            old_room.players.remove(player)

        # add player to new room        
        new_room.players.append(player)
        player.location = new_room.id

        # show new room
        player, world = await self.command.process_room(new_room_id, player, world)
        LogUtils.debug(f"{method_name}: exit", self.logger) 
        return player, world

    # just return the current date/time
    async def get_system_time(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        while True:
            time = datetime.datetime.now().strftime("%I:%M%p on %B %d")
            for world_player in self.players:
                time_event = TimeEvent(time).to_json()
                await self.utility.send_message_raw(time_event, world_player.websocket)
            
            # sleep 10 minutes
            await asyncio.sleep(60 * 10)

    # just returns a specific room in our list of rooms
    async def get_room(self, room_id):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)         
        room = [room for room in self.rooms_list if room.id == room_id][0]
        LogUtils.debug(f"{method_name}: exit, returning room \"{room.name}\"", self.logger)
        return room
