import asyncio
import json
from random import randint
from core.enums.events import EventEnum
from core.events.get_client import GetClientEvent
from core.events.username_request import UsernameRequestEvent
from core.locks import NpcLock
from core.objects.player import Player
from core.systems.emersion_events import EmersionEvents
from settings.world_settings import WorldSettings
from utilities.events import EventUtility
from utilities.exception import ExceptionUtility
from utilities.log_telemetry import LogTelemetryUtility


class World:
    def __init__(self, to_connections_queue: asyncio.Queue, to_world_queue: asyncio.Queue): 
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing WorldState() class")
        self.players = []
        self.monsters = []
        self.npcs = []
        self.rooms = []
        self.running_map_threads = []
        self.running_image_threads = []
        self.emersionEvents = EmersionEvents()
        self.to_connections_queue = to_connections_queue
        self.to_world_queue = to_world_queue

    async def setup_world(self):
        self.logger.debug("enter")
        asyncio.create_task(self.emersionEvents.setup())
        self.logger.debug("exit")

    # used to update webpage on user count
    async def update_website_users_online(self):
        self.logger.debug("enter")

        # Send the number of connected players to each player
        for player in self.players:
            try:
                await EventUtility.send_message(GetClientEvent(len(self.players)), player.websocket)
            except Exception as e:
                self.logger.error(
                    f"Error: {ExceptionUtility.get_exception_information(e)}"
                )
        self.logger.debug("exit")

    async def process_command(self, player, message):
        self.logger.debug(f"enter, message: {message}")

        # Parse the message as JSON
        data = json.loads(message.message) # this is the actual event from the client
        self.logger.debug(f"Parsed JSON data: {data}")

        # Handle different message types
        if data["type"] == EventUtility.get_event_type_id(EventEnum.COMMAND):
            command = data["cmd"]
            self.logger.info(f"Received command: {command}")
            await self.command.run_command(player, command, self.world_state)
        else:
            LogTelemetryUtility.warn(f"Unknown message type: {data['type']}")

    async def find_player_by_websocket(self, websocket):
        return next((p for p in self.players if p.websocket == websocket), None)
    
    async def process_connections_queue(self):
        while True:
            self.logger.debug("process_connections_queue waiting for message")
            message = await self.to_world_queue.get()
            self.logger.debug(f"World received message from connections: {message}")

            # assoiciate the message with the player
            player = await self.find_player_by_websocket(message.websocket)
            if not player and message.type == EventEnum.CONNECTION_NEW.value:
                player = Player(message.websocket)
                self.players.append(player)
                self.logger.debug(f"New player created: {player.name}")

                # request the player to send their name
                await EventUtility.send_message(
                    UsernameRequestEvent(WorldSettings.WORLD_NAME), player.websocket
                )
            else:
                # get the real message
                json_msg = json.loads(message.message)
                if player and json_msg["type"] == EventEnum.USERNAME_ANSWER.value:
                    player.name = json_msg["username"]      
                    self.logger.info(f"Player {player.name} connected. Total players: {len(self.players)}")          
                
                    # send the player
                    await EventUtility.send_message(GetClientEvent(len(self.players)), player.websocket)
                else:
                    # Process a generic command
                    await self.process_command(player, message)

            self.to_world_queue.task_done()

    async def check_monster_events(self):
        self.logger.debug("enter")
        while not self.shutdown:
            monsters = []

            # run events
            for monster in self.environments.all_monsters:
                # wander
                if monster.wanders:
                    monsters.append(asyncio.create_task(self.mob_wander(monster, is_npc=False)))

                # check for dialog
                monsters.append(asyncio.create_task(self.npc_dialog(monster)))

                # check for combat
                monsters.append(asyncio.create_task(self.npc_check_for_combat(monster)))

            await asyncio.gather(*monsters)

    async def check_npc_events(self):
        self.logger.debug("enter")
        while not self.shutdown:
            npcs = []

            # run events
            for npc in self.environments.all_npcs:
                # wander
                if npc.wanders:
                    npcs.append(asyncio.create_task(self.mob_wander(npc, is_npc=True)))

                # check for dialog
                npcs.append(asyncio.create_task(self.npc_dialog(npc)))

                # check for combat
                npcs.append(asyncio.create_task(self.npc_check_for_combat(npc)))

            await asyncio.gather(*npcs)

    async def mob_wander(self, mob, is_npc=True):
        self.logger.debug("enter")
        npclock = NpcLock(mob)
        async with npclock.lock:
            rand = randint(0, 10)
            self.logger.debug(f'NPC "{mob.name}" will move in {str(rand)} seconds...')
            await asyncio.sleep(rand)
            self = await mob.wander
