from core.enums.send_scope import SendScopeEnum
from core.interfaces.event import EventInterface
from utilities.log_telemetry import LogTelemetryUtility


class EventService:
    _instance = None
    logger = None

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = EventService()
        return cls._instance

    @staticmethod
    def instance():
        return EventService.get_instance()

    async def send_event(self, 
                         event: EventInterface, 
                         scope: SendScopeEnum, 
                         websocket=None, 
                         exclude_player=False,
                         player_data=None):
        msg = event.to_json()
        self.logger.debug(f"Sending event: {msg}, scope: {scope}, exclude_player: {exclude_player}, player_data: {player_data}")

        if scope == SendScopeEnum.PLAYER and websocket:
            await websocket.send(str(msg))
        elif scope == SendScopeEnum.ROOM and websocket:
            pass
            # origin_player_id = None
            # for player_id, data in player_data.items():
            #     if data["websocket"] == websocket:
            #         origin_player_id = player_id
            #         break
            # if origin_player_id:
            #     if player_data and player_data.get("room_id"):
            #         room_id = player_data["room_id"]
            #         player_ids_in_room = await self.world_service.get_players_in_room(room_id)
            #         for player_id in player_ids_in_room:
            #             if exclude_player and player_id == origin_player_id:
            #                 continue
            #             target_websocket = await self.world_service.get_player_websocket(player_id)
            #             if target_websocket:
            #                 await target_websocket.send(str(msg))
            #     else:
            #         print(f"Warning: Origin player {origin_player_id} not in a room.")
            # else:
            #     print(f"Warning: Origin websocket {websocket} not associated with a player.")
        elif scope == SendScopeEnum.ENVIRONMENT and websocket:
            pass
            # origin_player_id = None
            # for player_id, data in self.world_service.player_data.items():
            #     if data["websocket"] == websocket:
            #         origin_player_id = player_id
            #         break

            # if origin_player_id:
            #     player_data = self.world_service.player_data.get(origin_player_id)
            #     if player_data and player_data.get("environment_id"):
            #         environment_id = player_data["environment_id"]
            #         player_ids_in_environment = await self.world_service.get_players_in_environment(environment_id)
            #         for player_id in player_ids_in_environment:
            #             if exclude_player and player_id == origin_player_id:
            #                 continue
            #             target_websocket = await self.world_service.get_player_websocket(player_id)
            #             if target_websocket:
            #                 await target_websocket.send(str(msg))
            #     else:
            #         print(f"Warning: Origin player {origin_player_id} not in an environment.")
            # else:
            #     print(f"Warning: Origin websocket {websocket} not associated with a player.")
        elif scope == SendScopeEnum.WORLD:
            pass
            # all_websockets = await self.world_service.get_all_player_websockets()
            # for ws in all_websockets:
            #     if exclude_player:
            #         origin_player_id = None
            #         for player_id, data in self.world_service.player_data.items():
            #             if data["websocket"] == websocket:
            #                 origin_player_id = player_id
            #                 break
            #         if origin_player_id and self.world_service.get_player_websocket(origin_player_id) == ws:
            #             continue
            #     await ws.send(str(msg))
        else:
            raise ValueError(f"Invalid scope: {scope}")