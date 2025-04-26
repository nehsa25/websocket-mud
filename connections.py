import re
from tkinter import EventType
import websockets
from random import randint, choice
from core.enums.player_classes import PlayerClassEnum
from core.enums.eye_colors import EyeColorEnum
from core.enums.hair_colors import HairColorEnum
from core.enums.hair_lengths import HairLengthEnum
from core.enums.races import RaceEnum
from core.enums.scars import ScarEnum
from core.enums.tattoo_placements import TattooPlacementEnum
from core.enums.tattoo_severitities import TattooSeverityEnum
from core.events.announcement import AnnouncementEvent
from core.events.get_client import GetClientEvent
from core.events.inventory import InventoryEvent
from core.events.welcome import WelcomeEvent
from settings.world_settings import WorldSettings
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility
from utilities.exception import ExceptionUtility
from utilities.money import MoneyUtility
from utilities.wordsmith import Pronouns
import asyncio
import json
from utilities.command import Command


class Connection:
    def __init__(self, world, world_state):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.world = world
        self.world_state = world_state
        self.command = Command()

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
            await self.world_state.players.unregister(player, self.world_state)
        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")
        finally:
            self.logger.debug("exit")

    async def process_message(self, player, message):
        self.logger.debug(f"enter, player: {player.name}, message: {message}")

        # Parse the message as JSON
        data = json.loads(message)
        self.logger.debug(f"Parsed JSON data: {data}")

        # Handle different message types
        if data["type"] == EventUtility.get_event_type_id(EventTypes.COMMAND):
            command = data["cmd"]
            self.logger.info(f"Received command: {command}")
            await self.command.run_command(player, command, self.world_state)
        else:
            LogTelemetryUtility.warn(f"Unknown message type: {data['type']}")

    async def websocket_handler(websocket, path):
        while True:
            message = await websocket.recv()
            await websocket.send(f"Received message: {message}")

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

    # used to update webpage on user count
    async def update_website_users_online(self, world_state):
        self.logger.debug("enter")

        # Send the number of connected players to each player
        for player in self.players:
            try:
                await EventUtility.send_message(
                    GetClientEvent(len(self.players)), player.websocket
                )
            except Exception as e:
                self.logger.error(
                    f"Error: {ExceptionUtility.get_exception_information(e)}"
                )
        self.logger.debug("exit")

    async def register(self, player, world_state):
        self.logger.debug(f"enter, player: {player.name}")

        # if the name is empty, request another
        if not await self.check_valid_name(player.name):
            self.logger.debug(
                f"Name ({player.name}) is invalid, requesting a different one.."
            )
            await self.new_user(world_state, player.websocket, invalid_username=True)

        # if the name is already taken, request another
        matching_players = [p for p in self.players if p.name == player.name]
        if matching_players != []:
            self.logger.debug(
                f"Name ({matching_players[0].name}) is already taken, requesting a different one.."
            )
            await self.new_user(world_state, player.websocket, dupe=True)

        self.players.append(player)
        await self.update_website_users_online(world_state)

        # send msg to everyone
        for p in self.players:
            if p.name == player.name:
                await EventUtility.send_message(
                    WelcomeEvent(f"Welcome {player.name}!", player.name), p.websocket
                )
                await EventUtility.send_message(
                    InventoryEvent(player.inventory), p.websocket
                )
            else:
                await EventUtility.send_message(
                    AnnouncementEvent(f"{player.name} joined the game!"), p.websocket
                )
        self.logger.debug("exit")

        return player, world_state

    # calls at the beginning of the connection.  websocket connection here is the real connection
    async def new_user(
        self, world_state, websocket, dupe=False, invalid_username=False
    ):
        player = None

        self.logger.debug(
            f"enter, duplicate user flow: {dupe}, empty username flow: {invalid_username}"
        )
        self.logger.info(f"{websocket.remote_address}")
        ip = websocket.remote_address[0]
        self.logger.info("A new user has connected to NehsaMUD from {ip}")

        # get the client hostname
        self.logger.info("Requesting username")
        if dupe:
            await EventUtility.send_message(
                EventUtility.DuplicateNameEvent(), websocket
            )
        elif invalid_username:
            await EventUtility.send_message(EventUtility.InvalidNameEvent(), websocket)
        else:
            await EventUtility.send_message(
                EventUtility.UsernameRequestEvent(WorldSettings.WORLD_NAME), websocket
            )
        self.logger.info("Awaiting client name response from client..")
        msg = await websocket.recv()
        self.logger.info("Message received: {msg}")
        request = json.loads(msg)
        player_race = choice(list(RaceEnum))
        player_class = choice(list(PlayerClassEnum)).name
        player_intelligence = randint(1, 50)
        player_hp = randint(1, 50)
        player_strength = randint(1, 50)
        player_agility = randint(1, 50)
        player_location = world_state.environments.rooms[0]
        player_perception = randint(1, 50)
        player_faith = randint(1, 50)
        player_determination = randint(1, 50)
        age = randint(1, 75)
        level = randint(1, 75)
        pronoun = choice(list(Pronouns))

        inventory = Inventory(
            items=[],
            money=MoneyUtility(1000001),
            logger=self.logger,
        )

        # random characteristics
        eye_color = choice(list(EyeColorEnum)).name
        hair_color = choice(list(HairColorEnum)).name
        tattoes_placement = choice(list(TattooPlacementEnum)).name
        tattoes_severity = choice(list(TattooSeverityEnum)).name
        scars = choice(list(ScarEnum)).name
        hair_length = choice(list(HairLengthEnum)).name

        player = Player(
            eye_color=eye_color,
            hair_color=hair_color,
            hair_length=hair_length,
            tattoes_placement=tattoes_placement,
            tattoes_severity=tattoes_severity,
            scars=scars,
            name=request["username"],
            level=level,
            race=player_race,
            pronoun=pronoun,
            age=age,
            player_class=player_class,
            intelligence=player_intelligence,
            hp=player_hp,
            strength=player_strength,
            agility=player_agility,
            location_id=player_location,
            perception=player_perception,
            determination=player_determination,
            faith=player_faith,
            inventory=inventory,
            ip=ip,
            websocket=websocket,
        )

        if request["type"] == EventUtility.get_event_type_id(
            EventType.USERNAME_ANSWER
        ):
            await self.register(player, world_state)

            # move player to initial room
            player, world_state = await world_state.move_room_player(
                player.location_id, player
            )

            # send initial status
            await player.send_status()
        else:
            raise Exception(f"Shananigans? received request: {request['type']}")

        self.logger.debug("exit")
        return world_state

    # called when a client disconnects
    async def unregister(self, player, world_state, change_name=False):
        self.logger.debug(f"unregister: enter, player: {player.name}")
        self.logger.debug(f"self.players count: {len(self.players)}")
        self.players = [i for i in self.players if not i.websocket == player.websocket]
        await self.update_website_users_online(world_state)

        # let folks know someone left
        if change_name:
            await world_state.alert_world(
                f"{player.name} is changing their name..", player=player
            )
        else:
            await world_state.alert_world(
                f"{player.name} left the game.", player=player
            )

        self.logger.info(f"new player count: {len(self.players)}")
        self.logger.debug("register: exit")
        return world_state

    async def get_player(self, websocket):
        self.logger.debug("enter")
        player = None
        if self.players == []:
            return player

        for p in self.players:
            if p.websocket == websocket:
                player = p
                break
        self.logger.debug(f"exit, returning: {player.name}")
        return player

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
@staticmethod
async def start_websocket_server(mud, host, port):
    if host is None:
        async with websockets.serve(mud.main, "localhost", int(port), max_size=9000000):
            await asyncio.Future()  # Run forever
    else:
        async with websockets.serve(mud.main, host, int(port), max_size=9000000):
            await asyncio.Future()
