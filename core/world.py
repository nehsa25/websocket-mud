import asyncio
import json
from random import randint
from core.enums.events import EventEnum
from core.events.get_client import GetClientEvent
from core.locks import NpcLock
from core.objects.player import Player
from core.systems.emersion_events import EmersionEvents
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

    async def process_message(self, player, message):
        self.logger.debug(f"enter, player: {player.name}, message: {message}")

        # Parse the message as JSON
        data = json.loads(message)
        self.logger.debug(f"Parsed JSON data: {data}")

        # Handle different message types
        if data["type"] == EventUtility.get_event_type_id(EventEnum.COMMAND):
            command = data["cmd"]
            self.logger.info(f"Received command: {command}")
            await self.command.run_command(player, command, self.world_state)
        else:
            LogTelemetryUtility.warn(f"Unknown message type: {data['type']}")

    async def find_player_by_websocket(self, message):
        return [a for a in self.players if a.websocket == message["websocket"]]
    
    async def process_connections_queue(self):
        while True:
            self.logger.debug("process_connections_queue waiting for message")
            message = await self.to_world_queue.get()
            self.logger.debug(f"World received message from connections: {message}")

            # assoiciate the message with the player
            player = await self.find_player_by_websocket(message)
            if not player:
                # create new player
                player = Player(message["websocket"])

                self.players.append(player)
                self.logger.debug(f"New player created: {player.name}")
            

            # Process the message
            # await self.process_message(player, message)

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
