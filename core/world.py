import asyncio
import json
from random import randint
import re
from core.enums.environments import EnvironmentEnum
from core.enums.events import EventEnum
from core.enums.send_scope import SendScopeEnum
from core.events.duplicate_name import DuplicateNameEvent
from core.events.get_client import GetClientEvent
from core.events.info import InfoEvent
from core.events.invalid_name import InvalidNameEvent
from core.events.username_request import UsernameRequestEvent
from core.events.welcome import WelcomeEvent
from core.locks import NpcLock
from core.objects.player import Player
from core.systems.timeofday import TimeOfDay
from core.systems.emersion_events import EmersionEvents
from models.db_players import DBPlayer
from models.world_database import WorldDatabase
from services.auth import AuthService
from services.world import WorldService
from settings.world_settings import WorldSettings
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class World:
    def __init__(self, 
                 to_connections_queue: asyncio.Queue, 
                 to_world_queue: asyncio.Queue, 
                 world_service: WorldService):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing World")
        self.monsters = []
        self.npcs = []
        self.rooms = []
        self.running_map_threads = []
        self.running_image_threads = []
        self.emersionEvents = EmersionEvents()
        self.timeofDay = TimeOfDay()
        if not world_service:
            self.world_service = WorldService()
        self.world_database = WorldDatabase()
        
        self.auth_service = AuthService()
        self.to_connections_queue = to_connections_queue
        self.to_world_queue = to_world_queue

    async def start_world(self):
        self.logger.debug("enter")
        asyncio.create_task(self.emersionEvents.start())
        asyncio.create_task(self.timeofDay.start())
        # creates mobs
        # create weather

        self.logger.debug("exit")

    async def process_command(self, player, message):
        self.logger.debug(f"enter, message: {message}")

        # Parse the message as JSON
        data = json.loads(message.message)  # this is the actual event from the client
        self.logger.debug(f"Parsed JSON data: {data}")

        # Handle different message types
        if data["type"] == EventUtility.get_event_type_id(EventEnum.COMMAND):
            command = data["cmd"]
            self.logger.info(f"Received command: {command}")
            await self.command.run_command(player, command, self.world_state)
        else:
            self.logger.warn(f"Unknown message type: {data['type']}")

    async def find_player_by_websocket(self, websocket):
        return next((p for p in self.world_service.players if p == websocket.id.hex), None)

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

    async def process_connections_queue(self):
        while True:
            self.logger.debug("process_connections_queue waiting for message")
            message = await self.to_world_queue.get()
            self.logger.debug(f"World received message from connections: {message}")

            # assoiciate the message with the player
            player = await self.find_player_by_websocket(message.websocket)
            if not player and message.type == EventEnum.CONNECTION_NEW.value:
                self.world_service.players[message.websocket.id.hex] = None

                await InfoEvent("A user is logging in...").send(
                    websocket=message.websocket,
                    scope=SendScopeEnum.WORLD,
                    exclude_player=True,
                    player_data=self.world_service.players,
                )

                # register the player with the world service
                await self.world_service.register_player(
                    player, room_id=1, environment_id=EnvironmentEnum.TOWNSMEE.value, websocket=message.websocket
                )

                # request the player to send their name
                await UsernameRequestEvent(WorldSettings.WORLD_NAME).send(message.websocket)
            elif message.type == EventEnum.CLIENT_MESSAGE.value:
                # get the real type of the message
                json_msg = json.loads(message.message)
                if json_msg.get("type") == EventEnum.USERNAME_ANSWER.value:
                    # if the user has a token, we can validate it, other, assume they are new
                    if json_msg.get("token"):
                        is_valid = await self.auth_service.validate_token(json_msg["token"])
                        if not is_valid:
                            self.logger.debug(f"Invalid token: {json_msg['token']}")
                            await InvalidNameEvent(json_msg["username"]).send(message.websocket)
                            continue

                    else:
                        # validate name ok
                        is_ok = self.check_valid_name(json_msg["username"])
                        if not is_ok:
                            self.logger.debug(f"Invalid name: {json_msg['username']}")
                            await InvalidNameEvent(json_msg["username"]).send(message.websocket)
                            continue

                        # create new player
                        player = Player(json_msg["username"], message.websocket)

                        # generate a token for the player
                        player.token = self.auth_service.generate_token(json_msg["username"])

                        # update the db
                        self.world_service.players[message.websocket.id.hex] = await self.world_database.update_player(player)
                    
                    self.logger.info(f"New player {player.name} connected. Total players: {len(self.world_service.players)}")

                    await WelcomeEvent(f"Welcome {player.name}!", player.name, ).send(
                        player.websocket, scope=SendScopeEnum.PLAYER, player_data=self.world_service.players
                    )

                    # send the player
                    await GetClientEvent(len(self.world_service.players)).send(player.websocket)
                elif player and json_msg["type"] == EventEnum.ANNOUNCEMENT.value:
                    pass
                else:
                    # Process a in-game command
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
