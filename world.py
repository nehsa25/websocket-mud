import asyncio
import datetime
import inspect
from random import randint
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

    # schedule some events that'll do shit
    async def setup_world_events(self, logger):        
        if self.breeze_task == None:
            self.breeze_task = asyncio.create_task(self.breeze(logger))
            
        if self.rain_task == None:
            self.rain_task = asyncio.create_task(self.rain(logger))

        if self.eerie_task == None:
            self.eerie_task = asyncio.create_task(self.eerie_silence(logger))

        if self.thunder_task == None:
            self.thunder_task = asyncio.create_task(self.thunder(logger))

        if self.time_task == None:
            self.time_task = asyncio.create_task(self.get_system_time(logger))

    # It begins to rain..
    async def rain(self, logger):
        while True:
            rand = randint(2000, 3600*2)
            LogUtils.debug(f"Will run rain1 event in {str(rand)} seconds...", logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await Utility.send_msg("It begins to rain..", 'event', world_player.websocket, logger)

            # wait for it to stop
            rand = randint(100, 500)
            LogUtils.debug(f"Will run rain2 event in {str(rand)} seconds...", logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await Utility.send_msg("The rain pitter-patters to a stop and the sun begins to shine through the clouds..", 'event', world_player.websocket, logger)

    # You hear thunder off in the distane..
    async def thunder(self, logger):
        while True:
            rand = randint(2000, 3800*2)
            LogUtils.debug(f"Will run thunder event in {str(rand)} seconds...", logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await Utility.send_msg("You hear thunder off in the distance..", 'event', world_player.websocket, logger)

    # A gentle breeze blows by you..
    async def breeze(self, logger):        
        while True:
            rand = randint(2000, 3800*2)
            LogUtils.debug(f"Will run breeze event in {str(rand)} seconds...", logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await Utility.send_msg("A gentle breeze blows by you..", 'event', world_player.websocket, logger)

    # An eerie silence settles on the room..
    async def eerie_silence(self, logger):
        while True:
            rand = randint(2000, 4000*2)
            LogUtils.debug(f"Will run eerie_silence event in {str(rand)} seconds...", logger)
            await asyncio.sleep(rand)
            for world_player in self.players:
                await Utility.send_msg("An eerie silence settles on the room..", 'event', world_player.websocket, logger)

    # responsible for moving a player from one room to the next
    async def move_room(self, new_room_id, player, world, websocket, logger):
        old_room = await self.get_room(player.location)
        new_room = await self.get_room(new_room_id)

        if old_room != new_room:
            for monster in old_room["monsters"]:
                if monster.in_combat == player:
                    monster.in_combat = None

            # remove player from old room
            old_room['players'].remove(player)

        # add player to new room        
        new_room['players'].append(player)
        player.location = new_room["id"]

        # show new room
        return await Command.process_room(new_room_id, player, world, websocket, logger)

    # just return the current date/time
    async def get_system_time(self, logger):
        while True:
            time = datetime.datetime.now().strftime("%I:%M%p on %B %d")
            msg = f"It is {time}"
            for world_player in self.players:
                await Utility.send_msg(msg, 'time', world_player.websocket, logger)
            
            # sleep 10 minutes
            await asyncio.sleep(60 * 10)

    # just returns a specific room in our list of rooms
    async def get_room(self, room_id, logger=None):
        method_name = inspect.currentframe().f_code.co_name
        rooms = Rooms().all_rooms
        
        
        room = [room for room in rooms if room["id"] == room_id][0]
        LogUtils.debug(f"{method_name}: Returning room \"{room['name']}\"", logger)
        return room
