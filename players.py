import inspect
import json
from websockets import ConnectionClosedOK
from log_utils import LogUtils
from mudevent import MudEvents
from player import Player
from utility import Utility

class Players(Utility):
    logger = None
    players = []

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Admin() class", self.logger)
        self.utility = Utility(logger)

    # used to update webpage on user count
    async def update_website_users_online(self, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        get_client_event = world.players.GetClientEvent(len(self.players))
        for player in self.players:
            await self.utility.send_message(get_client_event, player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def register(self, player, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player.name}", self.logger)

        # if the name is already taken, request another
        matching_players = [p for p in self.players if p.name == player.name]
        if matching_players != []:
            LogUtils.debug(
                f"Name ({matching_players[0].name}) is already taken, requesting a different one..",
                self.logger,
            )
            await self.new_user(world, player.websocket, dupe=True)

        self.players.append(player)
        await self.update_website_users_online(world)

        # send msg to everyone
        for p in self.players:
            if p.name == player.name:
                await self.utility.send_message(MudEvents.WelcomeEvent(f"Welcome {player.name}!"), p.websocket)
            else:
                await self.utility.send_message(MudEvents.AnnouncementEvent(f"{player.name} joined the game!"), p.websocket)
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
            LogUtils.info(
                f"A new user has connected to NehsaMUD from {ip}", self.logger
            )

            # get the client hostname
            LogUtils.info(f"Requesting username", self.logger)
            if dupe:
                await self.utility.send_message(
                    MudEvents.DuplicateNameEvent(), websocket
                )
            else:
                await self.utility.send_message(
                    MudEvents.UsernameRequestEvent(), websocket
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
                request["username"],
                hp,
                strength,
                agility,
                location,
                perception,
                ip,
                websocket,
                self.logger,
            )

            if request["type"] == MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.USERNAME_ANSWER
            ):
                await self.register(player, world)

                # show room
                player, world = await world.rooms.move_room(player.location_id, player, world)
            else:
                raise Exception(f"Shananigans? received request: {request['type']}")

            LogUtils.debug(f"{method_name}: exit", self.logger)
        except ConnectionClosedOK:
            LogUtils.warn(f"ConnectionClosedOK ({player.name} left).", self.logger)
        except Exception as e:
            raise Exception(f"An error occurred during new_user(): {e}")

    # called when a client disconnects
    async def unregister(self, player, world, change_name=False):
        LogUtils.debug(f"unregister: enter, player: {player.name}", self.logger)
        LogUtils.debug(f"self.players count: {len(self.players)}", self.logger)
        self.players = [i for i in self.players if not i.websocket == player.websocket]
        await self.update_website_users_online(world)

        # let folks know someone left
        if change_name:
            await self.utility.alert_world(f"{player.name} is changing their name..", player, world)
        else:
            await self.utility.alert_world(f"{player.name} left the game.", player, world)

        LogUtils.info(f"new player count: {len(self.players)}", self.logger)
        LogUtils.debug(f"register: exit", self.logger)

    async def get_player(self, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        player = None
        if self.players == []:
            return player

        for p in self.players:
            if p.websocket == websocket:
                player = p
                break
        LogUtils.debug(f"{method_name}: exit, returning: {player.name}", self.logger)
        return player
