import inspect
import json

import jsonpickle
from websockets import ConnectionClosedOK
from log_utils import LogUtils, Level
from mudevent import DuplicateNameEvent, GetClientEvent, MudEvents, UsernameRequestEvent, WelcomeEvent
from player import Player
from utility import Utility


class Admin:
    logger = None
    utility = None

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Admin() class", self.logger)
        self.utility = Utility(self.logger)

    # used to update webpage on user count
    async def update_website_users_online(self, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        get_client_event = GetClientEvent(len(world.players)).to_json();
        for player in world.players:
            await self.utility.send_message_raw(get_client_event, player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def register(self, world, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player.name}", self.logger)

        # if the name is already taken, request another
        matching_players = [p for p in world.players if p.name == player.name]
        if matching_players != []:
            LogUtils.debug(
                f"Name ({matching_players[0].name}) is already taken, requesting a different one..",
                self.logger,
            )
            player, world = await self.new_user(world, player.websocket, True)

        world.players.append(player)
        await self.update_website_users_online(world)

        # send msg to everyone
        for world_player in world.players:
            if world_player.name == player.name:
                welcome_message = WelcomeEvent(f"Welcome {player.name}!").to_json()
                await self.utility.send_message_raw(welcome_message, world_player.websocket)
            else:
                welcome_message = WelcomeEvent(f"{player.name} joined the game!").to_json()
                await self.utility.send_message_raw(welcome_message, world_player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world

    # calls at the beginning of the connection.  websocket connection here is the real connection
    async def new_user(self, world, websocket, dupe=False):
        try:
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(
                f"{method_name}: enter, duplicate user flow: {dupe}", self.logger
            )
            LogUtils.info(f"{method_name}: {websocket.remote_address}", self.logger)
            ip = websocket.remote_address[0]
            LogUtils.info(f"A new user has connected to NehsaMUD from {ip}", self.logger)

            # get the client hostname
            LogUtils.info(f"Requesting username", self.logger)
            if dupe:
                await self.utility.send_message_raw(
                    DuplicateNameEvent().to_json(), websocket
                )
            else:
                await self.utility.send_message_raw(
                    UsernameRequestEvent().to_json(), websocket
                )
            LogUtils.info(f"Awaiting client name response from client..", self.logger)
            msg = await websocket.recv()
            LogUtils.info(f"Message received: {msg}", self.logger)
            request = json.loads(msg)
            hp = 50
            strength = 3  # 0 - 30
            agility = 3  # 0 - 30
            location = 0
            perception = 50
            player = Player(
                request["username"], hp, strength, agility, location, perception, ip, websocket, self.logger
            )

            if request["type"] == MudEvents.get_event_type_id(
                MudEvents.Event.USERNAME_ANSWER
            ):
                player, world = await self.register(world, player)

                # show room
                player, world = await world.move_room(player.location, player, world)
            else:
                LogUtils.error(
                    f"We shouldn't be here.. received request: {request['type']}",
                    self.logger,
                )

            LogUtils.debug(
                f"register: exit, returning: player: {player}, and world: {world} ",
                self.logger,
            )            
        except ConnectionClosedOK:
            LogUtils.warn(f"{player.name} left.", self.logger)            
        except Exception as e:
            LogUtils.error(f"new_user: {e}", self.logger, Level.ERROR)
        return player, world

    async def alert_world(self, world, message):
        LogUtils.debug(f"alert_world: enter, message: {message}", self.logger)
        for player in world.players:
            await self.utility.send_msg(message, "alert", player.websocket)
        LogUtils.debug(f"alert_world: exit", self.logger)

    # called when a client disconnects
    async def unregister(self, world, player, change_name=False):
        LogUtils.debug(f"unregister: enter, player: {player.name}", self.logger)
        LogUtils.debug(f"world.players count: {len(world.players)}", self.logger)
        world.players = [
            i for i in world.players if not i.websocket == player.websocket
        ]
        await self.update_website_users_online(world)

        # let folks know someone left
        if change_name:
            await self.alert_world(world, f"{player.name} is changing their name..")
        else:
            await self.alert_world(world, f"{player.name} left the game.")

        LogUtils.info(f"new player count: {len(world.players)}", self.logger)
        LogUtils.debug(f"register: exit, returning world: {world} ", self.logger)
        return world
