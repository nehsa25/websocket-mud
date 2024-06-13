import json
from log_utils import LogUtils, Level
from player import Player
from utility import Utility

class Admin:
    # used to update webpage on user count
    async def notify_users(world, logger):
        LogUtils.debug(f"notify_users: enter", logger)
        json_msg = {"type": "get_clients", "value": len(world.players)}

        LogUtils.debug(f"Sending json to each connected client: {json.dumps(json_msg)}", logger)
        for player in world.players:
            LogUtils.debug(f"Sending updated client list to {player.name}", logger)
            await player.websocket.send(json.dumps(json_msg))
            
        LogUtils.debug(f"notify_users: exit, returning: {world}", logger)
        return world
    
    @staticmethod
    async def register(world, request, player, websocket, logger):
        LogUtils.debug(f"add_user: enter: ", logger);
        LogUtils.debug(request, logger)
        player.name = request
        
        # if the name is already taken, request another
        matching_players = [p for p in world.players if p.name == player.name]
        if matching_players != []:
            LogUtils.debug(
                f"Name ({matching_players[0].name}) is already taken, requesting a different one..",
                logger,
            )
            return await Admin.new_user(websocket, logger, True)

        player.websocket = websocket
        world.players.append(player)
        await Admin.notify_users(world, logger)

        # send msg to everyone
        for world_player in world.players:
            if world_player.name == player.name:
                await Utility.send_msg(
                    f"Welcome {player.name}!", "welcome", websocket, logger
                )
            else:
                await Utility.send_msg(
                    f"{player.name} joined the game!",
                    "event",
                    world_player.websocket,
                    logger,
                )
        LogUtils.debug(f"add_user: exit, returning: {world}", logger)
        return world
    
    # calls at the beginning of the connection
    @staticmethod
    async def new_user(world, websocket, logger, dupe=False):
        LogUtils.debug(f"register: enter", logger)
        hp = 50
        strength = 3  # 0 - 30
        agility = 3  # 0 - 30
        location = 0
        perception = 50
        player = Player(hp, strength, agility, location, perception)

        LogUtils.debug(f"A new client has connected, registering..", logger)
        # get the client hostname
        LogUtils.debug(f"Requesting client hostname..", logger)
        if dupe:
            await websocket.send('{"type": "dupe_username"}')            
        else:
            await websocket.send('{"type": "request_hostname"}')
        LogUtils.debug(f"Awaiting client name response from client..", logger)
        msg = await websocket.recv()
        LogUtils.debug(f"Message received: {msg}", logger)
        request = json.loads(msg)
        ip = websocket.remote_address[0]
        LogUtils.debug("A new user has connected to NehsaMUD has connected: " + ip, logger)
        LogUtils.debug(
            f"Request received from {ip}: {request['type']}", logger
        )
        if request["type"] == "hostname_answer":
            world = await Admin.register(world, request["host"], player, websocket, logger) 

            # show room
            player, world = await world.move_room(
                player.location, player, world, websocket, logger
            )
        else:
            LogUtils.error(
                f"We shouldn't be here.. received request: {request['type']}",
                logger,
            )
            
        LogUtils.debug(f"register: exit, returning: player: {player}, and world: {world} ", logger)
        return player, world

    # called when a client disconnects
    @staticmethod
    async def unregister(world, websocket, logger, change_name = False):
        LogUtils.debug(f"unregister: enter", logger)
        current_player = [i for i in world.players if i.websocket == websocket][0]
        world.players = [
            i for i in world.players if not (i.websocket == websocket)
        ]
        world = await Admin.notify_users(world, logger)

        # let folks know someone left
        if change_name:
            for world_player in world.players:
                await Utility.send_msg(
                    f"{current_player.name} is changing their name..",
                    "event",
                    world_player.websocket,
                    logger,
                )
        else:
            for world_player in world.players:
                await Utility.send_msg(
                    f"{current_player.name} left the game.",
                    "event",
                    world_player.websocket,
                    logger,
                )
        LogUtils.debug(f"register: exit, returning world: {world} ", logger)
        return world
