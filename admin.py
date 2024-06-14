import inspect
import json
from log_utils import LogUtils, Level
from player import Player
from utility import Utility

class Admin:
    logger = None
    utility = None
    
    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.info("Initializing Admin() class", self.logger)
        self.utility = Utility(self.logger)
        
    # used to update webpage on user count
    async def notify_users(self, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)   
        json_msg = {"type": "get_clients", "value": len(world.players)}

        LogUtils.debug(f"Sending json to each connected client: {json.dumps(json_msg)}", self.logger)
        for player in world.players:
            LogUtils.debug(f"Sending updated client list to {player.name}", self.logger)
            await player.websocket.send(json.dumps(json_msg))
        LogUtils.debug(f"{method_name}: exit", self.logger)
    
    async def register(self, world, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player.name}", self.logger)   

        # if the name is already taken, request another
        matching_players = [p for p in world.players if p.name == player.name]
        if matching_players != []:
            LogUtils.debug(f"Name ({matching_players[0].name}) is already taken, requesting a different one..", self.logger,)
            player, world = await self.new_user(world, player.websocket, True)
        
        world.players.append(player)
        await self.notify_users(world)

        # send msg to everyone
        for world_player in world.players:
            if world_player.name == player.name:
                await self.utility.send_msg(f"Welcome {player.name}!", "welcome", world_player.websocket)
            else:
                await self.utility.send_msg(f"{player.name} joined the game!","event",world_player.websocket)
                
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world
    
    # calls at the beginning of the connection.  websocket connection here is the real connection
    async def new_user(self, world, websocket, dupe=False):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        LogUtils.debug(f"{method_name}: {websocket.remote_address}", self.logger)      
        ip = websocket.remote_address[0]
        LogUtils.debug(f"A new user has connected to NehsaMUD from {ip}", self.logger)

        # get the client hostname        
        if dupe:
            await websocket.send('{"type": "dupe_username"}')            
        else:
            LogUtils.debug(f"Requesting client hostname..", self.logger)
            await websocket.send('{"type": "request_hostname"}')
        LogUtils.debug(f"Awaiting client name response from client..", self.logger)
        msg = await websocket.recv()
        LogUtils.debug(f"Message received: {msg}", self.logger)
        request = json.loads(msg)
        hp = 50
        strength = 3  # 0 - 30
        agility = 3  # 0 - 30
        location = 0
        perception = 50
        player = Player(request["host"], hp, strength, agility, location, perception, ip, websocket)

        if request["type"] == "hostname_answer":
            player, world = await self.register(world, player) 

            # show room
            player, world = await world.move_room(player.location, player, world)
        else:
            LogUtils.error(f"We shouldn't be here.. received request: {request['type']}", self.logger)
            
        LogUtils.debug(f"register: exit, returning: player: {player}, and world: {world} ", self.logger)
        return player, world

    # called when a client disconnects
    async def unregister(self, world, websocket, change_name = False):
        LogUtils.debug(f"unregister: enter", self.logger)
        current_player = [i for i in world.players if i.websocket == websocket][0]
        world.players = [i for i in world.players if not (i.websocket == websocket)]
        await self.notify_users(world)

        # let folks know someone left
        if change_name:
            for world_player in world.players:
                await self.utility.send_msg(f"{current_player.name} is changing their name..","event", world_player.websocket)
        else:
            for world_player in world.players:
                await self.utility.send_msg(f"{current_player.name} left the game.","event",world_player.websocket)
        LogUtils.debug(f"register: exit, returning world: {world} ", self.logger)
        return world
