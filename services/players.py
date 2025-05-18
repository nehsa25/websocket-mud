import re
from typing import Dict, List, Optional, Set

from sqlalchemy import select
from core.data.player_data import PlayerData
from core.enums.send_scope import SendScopeEnum
from core.events.get_client import GetClientEvent
from core.events.username_request import UsernameRequestEvent
from models.db_players import DBPlayer
from models.world_database import WorldDatabase
from services.rooms import RoomRegistry
from settings.world_settings import WorldSettings
from utilities.log_telemetry import LogTelemetryUtility


class PlayerRegistry:
    players: Dict[str, PlayerData] = {}
    unsaved_players: Set[str] = set()

    def __init__(self, world_database: WorldDatabase, room_registry: RoomRegistry):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing PlayerRegistry")
        self.world_database = world_database
        self.room_players: Dict[str, Set[str]] = {}
        self.environment_players: Dict[str, Set[str]] = {}
        self.room_registry = room_registry
        
    async def get_all_db_players(self):
        ### called at the start of game to load all rooms into memory
        ### Get all rooms in the database

        players: Dict[str, PlayerData] = {}

        try:
            async with self.world_database.async_session() as session:
                async with session.begin():
                    player_result = await session.execute(select(DBPlayer))
                    tmp_players = player_result.scalars().all()

                    for p in tmp_players:
                        players[p.websocket_id] = p

        except Exception as e:
            self.logger.error(f"Error getting room: {e}")

        if players is None or len(players) == 0:
            raise Exception("Problem getting rooms from database.")

        self.players = players

    async def check_valid_name(self, name):
        self.logger.debug(f"Checking if name valid: {name}")

        name = name.strip()

        # eventually, this should be from npc and monster data
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

        self.logger.debug(f"exit, name valid: {valid}")
        return valid

    async def find_player_by_name(self, name):
        self.logger.debug(f"Finding player by name: {name}")
        item = next((p for p in self.players if self.players[p].name == name), None)
        self.logger.debug(f"Found player: {item}")
        return item
    
    async def register_player(self, websocket):
        self.logger.debug(f"Registering player: {websocket}")

        player = PlayerData(websocket=websocket)

        # used as an id for the player
        player_socket_id = websocket.id.hex
        player.websocket_id = player_socket_id

        # add to list
        self.players[player_socket_id] = player

        # request the player to send their name
        await UsernameRequestEvent(WorldSettings.WORLD_NAME).send(player.websocket)

        return player

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

    async def find_player_by_websocket_id(self, websocket_id):
        websocket_id = next(
            (
                a for a in self.players 
                if self.players[a] is not None and self.players[a].websocket_id == websocket_id
            ),
            None,
        )
        if websocket_id is not None:
            return self.players[websocket_id]
        return None
    
    def add_new_player(self, player: PlayerData):
        """Adds a new player to the registry (in-memory only initially)."""
        player_id = str(player.websocket_id)
        self.players[player_id] = player
        self.unsaved_players.add(player_id)
        self.logger.info(f"New player '{player_id}' added to registry (not yet saved).")

    def get_player(self, player_id: str) -> Optional[PlayerData]:
        """Retrieves a player from the registry by their ID."""
        return self.players.get(player_id)

    def get_players(self) -> List[PlayerData]:
        """Retrieves all players in the registry."""
        return list(self.players.values())

    async def save_player(self, player: PlayerData):
        """Saves a specific player's data to the database."""
        db_player = player.to_database()
        try:
            async with self.world_database.async_session() as session:
                async with session.begin():
                    session.add(db_player)
                    await session.commit()
            player_id = str(player.id)
            if player_id in self.unsaved_players:
                self.unsaved_players.remove(player_id)
            self.logger.info(f"Player '{player.selected_character.name}' saved to the database.")
        except Exception as e:
            self.logger.error(f"Error saving player '{player.selected_character.name}': {e}")

    async def save_unsaved_players(self):
        """Saves all players currently marked as unsaved to the database."""
        players_to_save = [self.players[player_id] for player_id in self.unsaved_players]
        if not players_to_save:
            self.logger.info("No new players to save.")
            return

        try:
            async with self.world_database.async_session() as session:
                async with session.begin():
                    db_players = [player.to_database() for player in players_to_save]
                    session.add_all(db_players)
                    await session.commit()
            self.unsaved_players.clear()
            self.logger.info(f"Saved {len(players_to_save)} new players to the database.")
        except Exception as e:
            self.logger.error(f"Error saving unsaved players: {e}")

    async def remove_player(self, player_id: str):
        """Removes a player from the registry and potentially the database."""
        if player_id in self.players:
            player = self.players.pop(player_id)
            if player_id in self.unsaved_players:
                self.unsaved_players.remove(player_id)
            else:
                # Optionally, you could also delete from the database here if needed
                self.logger.warning(f"Player '{player.selected_character.name}' removed from registry (database entry remains).")
        else:
            self.logger.warning(f"Player with ID '{player_id}' not found in registry.")

    async def add_player_to_room(self, player_id: str, room_id: str):
        if room_id not in self.room_players:
            self.room_players[room_id] = set()
        self.room_players[room_id].add(player_id)

    async def remove_player_from_room(self, player_id: str, room_id: str):
        if room_id in self.room_players and player_id in self.room_players[room_id]:
            self.room_players[room_id].remove(player_id)
            if not self.room_players[room_id]:
                del self.room_players[room_id]

    async def get_players_in_room(self, room_id: str) -> Set[PlayerData]:
        player_ids = self.room_players.get(room_id, set())
        return {self.players[pid] for pid in player_ids if pid in self.players}

    async def add_player_to_environment(self, player_id: str, environment_id: str):
        if environment_id not in self.environment_players:
            self.environment_players[environment_id] = set()
        self.environment_players[environment_id].add(player_id)

    async def remove_player_from_environment(self, player_id: str, environment_id: str):
        if environment_id in self.environment_players and player_id in self.environment_players[environment_id]:
            self.environment_players[environment_id].remove(player_id)
            if not self.environment_players[environment_id]:
                del self.environment_players[environment_id]

    async def get_players_in_environment(self, environment_id: str) -> Set[PlayerData]:
        player_ids = self.environment_players.get(environment_id, set())
        return {self.players[pid] for pid in player_ids if pid in self.players}
