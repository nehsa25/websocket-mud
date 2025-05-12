from typing import Dict, Set
from core.data.environment_data import EnvironmentData
from core.data.room_data import RoomData
from core.enums.send_scope import SendScopeEnum
from core.events.get_client import GetClientEvent
from core.events.username_request import UsernameRequestEvent
from core.objects.player import Player
from services.image import ImageService
from services.map import MapService
from settings.world_settings import WorldSettings
from utilities.log_telemetry import LogTelemetryUtility


class WorldService:
    _instance = None

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing WorldService")
        self.players: Dict[str, Player] = {}
        self.room_players: Dict[str, Set[str]] = {}
        self.environment_players: Dict[str, Set[str]] = {}
        self.rooms: Dict[str, RoomData] = {}
        self.environments: Dict[str, EnvironmentData] = {}
        self.image_service = ImageService()
        self.map_service = MapService()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = WorldService()
        return cls._instance

    @staticmethod
    def instance():
        return WorldService.get_instance()

    async def register_player(self, websocket, room_id, environment_id):
        self.logger.debug(f"Registering player: {websocket} in room {room_id} and environment {environment_id}")

        player = Player(websocket)

        player_socket_id = websocket.id.hex

        # get room
        player.room = self.get_room(room_id)

        player.socket_id = player_socket_id

        # Track players in rooms
        if room_id not in self.room_players:
            self.room_players[room_id] = set()
        self.room_players[room_id].add(player_socket_id)

        # Track players in environments
        if environment_id not in self.environment_players:
            self.environment_players[environment_id] = set()
        self.environment_players[environment_id].add(player_socket_id)

        # generate map event
        # await self.map_service.generate_map()

        # generate room image event
        # await self.image_service.generate_image()

        # add to list
        self.players[player_socket_id] = player

        # request the player to send their name
        await UsernameRequestEvent(WorldSettings.WORLD_NAME).send(player.websocket)

    async def unregister_player(self, player_id):
        if player_id in self.players:
            player = self.players.pop(player_id)
            room_id = player.room_id
            environment_id = player.environment_id

            # Remove player from room tracking
            if room_id in self.room_players:
                self.room_players[room_id].discard(player_id)

            # Remove player from environment tracking
            if environment_id in self.environment_players:
                self.environment_players[environment_id].discard(player_id)

            await GetClientEvent(len(self.players)).send(player.websocket, scope=SendScopeEnum.WORLD)

    async def get_player_websocket(self, player_id):
        return next(
            (
                a
                for a in self.world_service.players
                if self.world_service.players[a] is not None
                and self.world_service.players[a].websocket == player_id
            ),
            None,
        )

    async def get_players_in_room(self, room_id):
        return list(self.room_players.get(room_id, []))

    async def get_players_in_environment(self, environment_id):
        return list(self.environment_players.get(environment_id, []))

    async def get_all_player_websockets(self):
        return [player.websocket for player in self.players.values()]

    # Methods to manage rooms and environments (optional but good practice)
    def add_room(self, room: RoomData):
        if room.room_id not in self.rooms:
            self.rooms[room.room_id] = room

    def get_room(self, room_id: str) -> RoomData | None:
        return self.rooms.get(room_id)

    def add_environment(self, environment: EnvironmentData):
        if environment.environment_id not in self.environments:
            self.environments[environment.environment_id] = environment

    def get_environment(self, environment_id: str) -> EnvironmentData | None:
        return self.environments.get(environment_id)