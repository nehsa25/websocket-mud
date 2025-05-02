import re
import websockets
from core.enums.events import EventEnum
from core.events.client_message import ClientMessageEvent
from core.events.connection import ConnectionEvent
from core.events.connection_new import NewConnectionEvent
from core.events.duplicate_name import DuplicateNameEvent
from core.events.info import InfoEvent
from core.events.invalid_name import InvalidNameEvent
from core.events.invalid_token import InvalidTokenEvent
from core.events.username_request import UsernameRequestEvent
from core.events.welcome import WelcomeEvent
from settings.world_settings import WorldSettings
from utilities.auth import Auth
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility
from utilities.exception import ExceptionUtility
import asyncio
import json
from utilities.command import Command


class Connections:
    connections = []

    def __init__(self, to_connections_queue: asyncio.Queue, to_world_queue: asyncio.Queue): 
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.command = Command()
        self.from_world_queue = to_world_queue
        self.to_world_queue = to_connections_queue

    async def connection_loop(self, websocket):
        try:
            self.logger.info("A connection was made!")
            msg = NewConnectionEvent(websocket)
            await self.to_world_queue.put(msg)

            while True:
                client_message = await websocket.recv()
                await self.to_world_queue.put(ClientMessageEvent(client_message, websocket))

        except Exception as e:
            self.logger.error(f"Error in connection loop: {e}")
        finally:
            self.logger.info("Connection ended.")

    async def handle_connection(self, player, websocket):
        self.logger.debug(f"enter, player: {player}")
        try:
            while True:
                # Receive data from the client
                message = await websocket.recv()
                self.logger.debug(f"Received message: {message}")

                # Process the message
                await self.process_message(player, message)

        except websockets.ConnectionClosedOK:
            LogTelemetryUtility.warn("ConnectionClosedOK (client disconnected).")
            await self.unregister(player, self.world_state)
        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")
        finally:
            self.logger.debug("exit")

    async def exit_handler(self, signal, frame):
        self.logger.debug(f"enter, signal: {signal}, frame: {frame}")
        self.logger.info("An exit signal as been received.  Exiting!")
        # exit stuff..
        self.logger.debug("exit")

    async def check_valid_name(self, name):
        self.logger.debug("enter")

        name = name.strip()

        problem_names = [
            "",
            "admin",
            "administrator",
            "moderator",
            "map",
            "help",
            "look",
            "inv",
            "inventory",
            "quit",
            "exit",
            "sys",
            "system",
            "god",
            "superuser",
            "super",
            "nehsa",
            "nehsamud",
            "nehsa_mud",
            "candie",
            "princess candie",
            "renkath",
            "cog",
            "frederick",
            "jaque",
            "maximus",
        ]

        valid = True

        # the name must:
        # - be between 3 and 25 characters
        # - not contain any special characters
        # - not be a problem name
        # - but can have spaces "Hink the Great"
        if len(name) < 3 or len(name) > 25 or not re.match(r"^[a-zA-Z0-9\s]+$", name):
            valid = False

        # tests:
        # "Hink" - valid
        # "hink" - valid
        # "Hink the Great" - valid
        # "" - invalid
        # " Hink" - invalid

        if name.lower() in problem_names:
            valid = False

        self.logger.debug(f"exit, returning: {valid}")
        return valid

    async def register(self, request, websocket):
        self.logger.debug(f"enter, request: {request['username']}")


        # # if the name is already taken, request another
        # matching_players = [p for p in self.players if p.name == request["username"]]
        # if matching_players != []:
        #     self.logger.debug(
        #         f"Name ({matching_players[0].name}) is already taken, requesting a different one.."
        #     )
        #     await self.new_user(websocket, dupe=True)

        # Send asyncio queue to world with request information so a new player can be created
        self.logger.debug(f"Creating new player: {request['username']}")        
        player_data = {
            "username": request["username"],
            "websocket": websocket, 
            "ip": websocket.remote_address,
            "token": request["token"]
        }
        await self.to_world_queue.put({"type": "CREATE_PLAYER", "player_data": player_data})

        await EventUtility.send_message(
            WelcomeEvent(f"Welcome {request['username']}!", request["username"]), websocket
        )

        self.logger.debug("exit")

    async def check_username_in_use(self, request, websocket):
        self.logger.debug(f"enter, request: {request['username']}")
        in_use = False
        
        player_data = {
            "username": request["username"],
            "websocket": websocket, 
            "ip": websocket.remote_address,
            "token": request["token"]
        }
        connectionEvent = ConnectionEvent(
            event_type=EventEnum.PLAYER_CHECK_DUPLICATE,
            message=player_data
        )
        await self.from_world_queue.put(connectionEvent.to_json())
        
        # wait for a response from the world
        while True:
            if not self.to_world_queue.empty():
                world_message = await self.to_world_queue.get()
                self.logger.debug(f"Received message from world: {world_message}")
                if world_message["type"] == EventEnum.PLAYER_CHECK_DUPLICATE:
                    break
                self.to_world_queue.task_done()

        # check if the name is in use
        if world_message["in_use"]:
            in_use = True

        self.logger.debug("exit")
        return in_use

    # calls at the beginning of the connection.  websocket connection here is the real connection
    async def new_connection(self, websocket, dupe=False, invalid_username=False
    ):
        self.logger.debug(f"enter, duplicate user flow: {dupe}, empty username flow: {invalid_username}")
        self.logger.info("A new user has connected to NehsaMUD from {ip}")

        # get the client hostname
        self.logger.info("Requesting username")
        await EventUtility.send_message(
            event_object=UsernameRequestEvent(WorldSettings.WORLD_NAME), 
            websocket=websocket
        )

        self.logger.info("Awaiting username response from client..")
        msg = await websocket.recv()
        self.logger.info("Message received: {msg}")
        request = json.loads(msg)

        if request["type"] == EventUtility.get_event_type_id(EventEnum.USERNAME_ANSWER):
            self.logger.debug("username answer received")
            
            # check if token exists of if this is new user 
            if "token" in request:
                # check if token is valid
                if not Auth.validate_token(request["token"]):
                    self.logger.debug("token is invalid")
                    await EventUtility.send_message(InvalidTokenEvent(), websocket)
                    return
            else:
                # generate a new token
                request["token"] = Auth.generate_token(request["username"])

            # validate the username
            valid = await self.check_valid_name(request["username"])
            if not valid:
                self.logger.debug("username is invalid")
                await EventUtility.send_message(InvalidNameEvent(), websocket)
                return
            
            # validate name not already taken
            in_use = await self.check_username_in_use(request, websocket)
            if in_use:
                self.logger.debug("username is already in use")
                await EventUtility.send_message(DuplicateNameEvent(), websocket)
                return
            
            await self.register(request, websocket)
        else:
            raise Exception(f"Shananigans? received request: {request['type']}")

        self.logger.debug("exit")

    # called when a client disconnects
    async def unregister(self, player, world_state, change_name=False):
        self.logger.debug(f"unregister: enter, player: {player.name}")
        self.logger.debug(f"self.players count: {len(self.players)}")
        self.players = [i for i in self.players if not i.websocket == player.websocket]
        await self.update_website_users_online(world_state)

        # # let folks know someone left
        # if change_name:
        #     await world_state.alert_world(
        #         f"{player.name} is changing their name..", player=player
        #     )
        # else:
        #     await world_state.alert_world(
        #         f"{player.name} left the game.", player=player
        #     )

        self.logger.info(f"new player count: {len(self.players)}")
        self.logger.debug("register: exit")
        return world_state

    # async def get_player(self, websocket):
    #     self.logger.debug("enter")
    #     player = None
    #     if self.players == []:
    #         return player

    #     for p in self.players:
    #         if p.websocket == websocket:
    #             player = p
    #             break
    #     self.logger.debug(f"exit, returning: {player.name}")
    #     return player

    async def find_player_by_name(self, name):
        self.logger.debug("enter")
        player = None
        if self.players == []:
            return player

        for p in self.players:
            if p.name == name:
                player = p
                break
        self.logger.debug(f"exit, returning: {player.name}")
        return player

    # start websocket server
    async def start_websocket_server(self, mud, host, port):
        if host is None:
            async with websockets.serve(mud.main, "localhost", int(port), max_size=9000000):
                await asyncio.Future()  # Run forever
        else:
            async with websockets.serve(mud.main, host, int(port), max_size=9000000):
                await asyncio.Future()
