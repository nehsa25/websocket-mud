import asyncio
import json
from core.enums.events import EventEnum
from core.enums.rooms import RoomEnum
from core.enums.send_scope import SendScopeEnum
from core.events.get_client import GetClientEvent
from core.events.info import InfoEvent
from core.events.invalid_name import InvalidNameEvent
from core.events.room import RoomEvent
from core.events.welcome import WelcomeEvent
from core.systems.timeofday import TimeOfDay
from core.systems.emersion_events import EmersionEvents
from models.world_database import WorldDatabase
from queues.game_message import GameMessage
from services.auth import AuthService
from services.image import ImageService
from services.map import MapService
from services.world import WorldService
from settings.world_settings import WorldSettings
from utilities.command import CommandHandler
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class World:
    def __init__(self, to_connections_queue: asyncio.Queue, to_world_queue: asyncio.Queue):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing World")
        self.monsters = []
        self.npcs = []
        self.rooms = []
        self.running_map_threads = []
        self.running_image_threads = []
        self.to_connections_queue = to_connections_queue
        self.to_world_queue = to_world_queue
        self.world_database = WorldDatabase()
        self.world_service = WorldService(self.world_database)
        self.auth_service = AuthService()
        self.command = CommandHandler()
        self.emersionEvents = EmersionEvents(self.world_service)
        self.timeofDay = TimeOfDay(self.world_service)
        self.image_service = ImageService(self.world_service)
        self.map_service = MapService(self.world_service)

    async def start_world(self):
        self.logger.debug(f"Starting the world of {WorldSettings.WORLD_NAME}...")

        await self.world_service.setup_state_data()
        asyncio.create_task(self.emersionEvents.start())
        asyncio.create_task(self.timeofDay.start())
        # creates mobs
        # create weather

        self.logger.debug("exit")

    async def process_messages(self):
        while True:
            self.logger.debug("process_connections_queue waiting for message")
            message: GameMessage = await self.to_world_queue.get()
            self.logger.debug(f"World received message from connections: {message.type}, origin: {message.origin}")

            # associate the message with the player
            websocket_id = message.websocket.id.hex
            player = await self.world_service.player_registry.find_player_by_websocket_id(websocket_id)
            player_socket_id = websocket_id

            # connection_new comes from connections.py when we first receve a websocket connection
            if not player and message.type == EventEnum.CONNECTION_NEW.value:
                await InfoEvent("A user is logging in...").send(
                    websocket=message.websocket,
                    scope=SendScopeEnum.WORLD,
                    exclude_player=True,
                    player_data=self.world_service.player_registry,
                )

                # register the player with the world service
                player = await self.world_service.player_registry.register_player(message.websocket)
                if not player:
                    raise Exception("Player not registered")

                self.logger.debug(f"New player registered: {player}")
            elif message.type == EventEnum.CLIENT_MESSAGE.value:
                # get the real type of the message
                json_msg = json.loads(message.payload)
                if json_msg.get("type") == EventEnum.USERNAME_ANSWER.value:
                    wanted_username = json_msg["username"]

                    if wanted_username == "guest":
                        room = await self.world_service.room_registry.get_room_by_id(RoomEnum.TOWNSMEE_TOWNSQUARE.value)
                        await player.create_character(
                            firstname="Guest",
                            lastname="Character",
                            room=room,
                        )

                    # validate name ok
                    is_ok = await self.world_service.player_registry.check_valid_name(wanted_username)
                    if not is_ok:
                        self.logger.debug(f"Invalid name: {wanted_username}")
                        await InvalidNameEvent(wanted_username).send(message.websocket)
                        continue

                    # if this is an answer, we should already have a player object
                    player = await self.world_service.player_registry.find_player_by_websocket_id(
                        message.websocket.id.hex
                    )
                    if player:
                        self.logger.debug(
                            f"Player found: {player}, looking for characters with name: {wanted_username}"
                        )
                        if player.characters is None or len(player.characters) == 0:
                            raise Exception(f"Player {player.selected_character.name} has no characters.")

                        player.selected_character = player.characters[0]
                        self.logger.debug(
                            f"Player updated. Selected user: {player.selected_character.name}, websocket: {player.websocket.id.hex}"
                        )

                        self.world_service.player_registry.add_new_player(player)
                        self.logger.debug(
                            f"Player updated in world service: {self.world_service.player_registry.players[player_socket_id]}"
                        )
                    else:
                        raise Exception(f"Player with websocket {message.websocket} not found for name update.")

                    # if the user has a token, we can validate it, otherwise, assume they are new
                    if json_msg.get("token"):
                        is_valid = self.auth_service.validate_token(json_msg["token"])
                        if is_valid:
                            # if the token is valid but we see a player is already using the name, we can assume this is a browser refresh
                            # and we can just   refresh the player with the new websocket
                            found_player_socket_id = await self.world_service.player_registry.find_player_by_name(
                                json_msg["username"]
                            )
                            if (
                                found_player_socket_id
                                and self.world_service.player_registry[found_player_socket_id].websocket_id
                                != player_socket_id
                            ):
                                self.logger.debug(
                                    "Player likely pressed refresh (F5). Updating existing player websocket information."
                                )
                                player.websocket = message.websocket
                                player.token = json_msg.get("token")
                                self.world_service.player_registry[player_socket_id] = player

                                # remove bad player from the world service
                                if len(self.world_service.player_registry) > 0:
                                    del self.world_service.player_registry[found_player_socket_id]

                                # update the db
                                await self.world_database.update_player(player)
                        else:
                            self.logger.debug(f"Invalid token: {json_msg.get('token')}")
                            await InvalidNameEvent(json_msg["name"]).send(message.websocket)
                            continue
                    else:
                        # generate a token for the player
                        player.token = self.auth_service.generate_token(json_msg["username"])

                        # update the player in the world service
                        self.world_service.player_registry.players[player_socket_id] = player

                    self.logger.info(
                        f"New player {player.selected_character.name} connected. Total players: {len(self.world_service.player_registry.players)}"
                    )

                    # send the welcome message to user and all other players
                    await WelcomeEvent(player.selected_character, player.token).send(
                        player.websocket,
                        scope=SendScopeEnum.PLAYER,
                        player_data=self.world_service.player_registry.players,
                    )

                    # send the player information about who is in the game
                    await GetClientEvent(len(self.world_service.player_registry.players)).send(player.websocket)

                    # if the player has more than one character,select first and they can change later
                    player.selected_character = player.characters[0] if len(player.characters) > 0 else None

                    # get room information from room_registry
                    room = await self.world_service.room_registry.get_room_by_id(player.selected_character.room_id)
                    if not room:
                        raise Exception(f"Room with id {player.room_id} not found in room registry.")

                    # send the room
                    await RoomEvent(room).send(
                        player.websocket,
                    )

                elif player and json_msg["type"] == EventEnum.NEW_USER.value:
                    await self.world_database.update_player(player)
                else:
                    # Process a in-game command
                    await self.process_command(player, message)

            self.to_world_queue.task_done()

    # this is a game command such as look, get, drop, etc.
    async def process_command(self, player, message):
        self.logger.debug(f"enter, message: {message}")

        # Parse the message as JSON
        data = json.loads(message.payload)  # this is the actual event from the client
        self.logger.debug(f"Parsed JSON data: {data}")

        # Handle different message types
        if data["type"] == EventUtility.get_event_type_id(EventEnum.COMMAND):
            cmd = data["cmd"]
            self.logger.info(f"Received command: {cmd}")
            await self.command.run_command(player, cmd)
        else:
            self.logger.warn(f"Unknown message type: {data['type']}")
