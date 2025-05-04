from core.enums.send_scope import SendScopeEnum
from core.events.get_client import GetClientEvent


class WorldService:
    _instance = None

    def __init__(self):
        self.player_data = {}  # player_id: {"websocket": websocket, "room_id": room_id, "environment_id": environment_id}
        self.room_players = {}  # room_id: set of player_ids
        self.environment_players = {}  # environment_id: set of player_ids

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = WorldService()
        return cls._instance

    @staticmethod
    def instance():
        return WorldService.get_instance()

    async def register_player(self, player_id, websocket, room_id, environment_id):
        self.player_data[player_id] = {"websocket": websocket, "room_id": room_id, "environment_id": environment_id}
        if room_id not in self.room_players:
            self.room_players[room_id] = set()
        self.room_players[room_id].add(player_id)
        if environment_id not in self.environment_players:
            self.environment_players[environment_id] = set()
        self.environment_players[environment_id].add(player_id)

    async def unregister_player(self, player_id):
        if player_id in self.player_data:
            data = self.player_data.pop(player_id)
            room_id = data.get("room_id")
            environment_id = data.get("environment_id")
            if room_id in self.room_players:
                self.room_players[room_id].discard(player_id)
            if environment_id in self.environment_players:
                self.environment_players[environment_id].discard(player_id)
            await GetClientEvent(len(self.players)).send(data.websocket, scope=SendScopeEnum.WORLD)

    async def get_player_websocket(self, player_id):
        data = self.player_data.get(player_id)
        return data.get("websocket") if data else None

    async def get_players_in_room(self, room_id):
        return list(self.room_players.get(room_id, []))

    async def get_players_in_environment(self, environment_id):
        return list(self.environment_players.get(environment_id, []))

    async def get_all_player_websockets(self):
        return [data["websocket"] for data in self.player_data.values()]