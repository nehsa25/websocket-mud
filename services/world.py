from __future__ import annotations
from typing import Dict
from core.data.environment_data import EnvironmentData
from models.world_database import WorldDatabase
from services.players import PlayerRegistry
from services.rooms import RoomRegistry
from utilities.log_telemetry import LogTelemetryUtility


class WorldService:
    _instance = None
    room_registry: RoomRegistry = None

    def __init__(self, world_database: WorldDatabase):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing WorldService")
        self.world_database = world_database
        self.room_registry = RoomRegistry(self.world_database)
        self.player_registry = PlayerRegistry(self.world_database, self.room_registry)
        self.environments: Dict[str, EnvironmentData] = {}

    async def setup_state_data(self):
        self.logger.debug("Setting up state data...")

        # we need to get all the data in memory at the start so we have can modify their state
        await self.room_registry.get_all_db_rooms()
        # await self.player_registry.get_all_db_players() - this doesn't make sense as there's no active websocket

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = WorldService()
        return cls._instance

    @staticmethod
    def instance():
        return WorldService.get_instance()

    def add_environment(self, environment: EnvironmentData):
        if environment.environment_id not in self.environments:
            self.environments[environment.environment_id] = environment

    def get_environment(self, environment_id: str) -> EnvironmentData | None:
        return self.environments.get(environment_id)
