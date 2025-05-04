import random
import time
from enums.alignments import Alignment
from events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
from ai.dialog import NpcDialog


class Mob:
    name = ""
    title = ""
    description = ""
    common_phrases = []
    interests = []
    schedules = []
    wander_event = None
    last_direction = None
    wanders = False
    room_id = None
    prev_room_id = None
    last_check_combat = None
    alignment = None
    in_combat = False

    def __init__(self, name="", description="", title=""):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Npc() class")
        if name == "":
            self.name = self.generate_name(include_identifier=False)
        else:
            self.name = name

        self.title = title
        self.description = description
        self.alignment = Alignment.NEUTRAL
        self.dialog = NpcDialog()

    # announce we're here!
    async def announce_entrance(self, room):
        # eventually we can use the room to indicate which direciton the monster came from/going to
        return self.entrance_cry

    async def stop_combat(self, player):
        pass

    async def break_combat(self, room):
        pass

    async def kill(self, room):
        self.is_alive = False
        self.dead_epoch = int(time.time())

        if self.death_cry is not None:
            for player in room["players"]:
                await InfoEvent(self.death_cry).send(player.websocket)

    # respawn mobs after a certain amount of time
    async def respawn(self, world_state):
        self.logger.info(f"{self.name} checking for respawn: {world_state}")

        # # look through each room
        # for room in rooms:
        #     # and if the room has monsters
        #     if len(room.monsters) > 0:
        #         for monster in room.monsters:
        #             # check if they're dead
        #             if monster.is_alive is False:
        #                 current_epoch = int(time.time())

        #                 # if monster has been dead for more than monster.respawn_rate_secs, remove it and create new monster
        #                 # (we should consider making then kinda random (2-5 minutes for example))
        #                 secs_since_death = current_epoch - monster.dead_epoch
        #                 if secs_since_death >= monster.respawn_rate_secs:
        #                     # remove old monster
        #                     self.logger.debug(
        #                         f'Removing "{monster.name}" from room',
        #                         self.logger,
        #                     )
        #                     room.monsters.remove(monster)

        #                     # create new monster
        #                     new_monster = await self.world.monsters.get_monster(
        #                         monster.monster_type, room, self.logger
        #                     )
        #                     self.logger.info(
        #                         f'Respawning "{new_monster.name}" in room {room.id} ({room.name})',
        #                         self.logger,
        #                     )
        #                     room.monsters.append(new_monster)

    def get_attack_phrase(self, target):
        npc_attack_templates = [
            f"{self.name} alters course to intercept {target}!",
            f"{self.name} moves to attack {target}!",
            f"{self.name} moves to block {target}'s path!",
        ]
        return random.choice(npc_attack_templates)

    def get_full_name(self):
        return f"{self.title} {self.name}".strip()

    def generate(self):
        self.logger.info(f"Generating Npc {self.name}...")
        return self

    # responsible for moving npc
    async def wander(self, world_state, is_npc):
        self.logger.debug(f"enter: {self.name}")
        if not self.wanders:
            self.logger.info(f"{self.name} - I don't wander")
            return

        self.logger.debug(f"NPC {self.name} wandering!")

        # get random direction
        direction = None
        room = await world_state.get_room(self.room_id)
        if self.last_direction is None:
            direction = random.choice(room.exits)
        else:
            found_direction = False
            while not found_direction:
                direction = random.choice(room.exits)
                if direction != self.last_direction or len(room.exits) == 1:
                    found_direction = True

        if direction is None or direction == []:
            raise Exception(f"{self.name} - No exits found")

        self, world_state = await self.move(direction, world_state, is_npc)
        self.last_direction = direction

        self.logger.debug("exit")
        return world_state

    # responsible for checking combat
    async def check_combat(self, world_state):
        pass

    # check for dialog options
    async def speak(self, room, world_state):
        self.logger.debug("enter")

        # gather things we may be interested in
        # num players
        # num monsters
        # num other npcs
        # time of day
        # weather
        # room description
        # room exits
        # room items

        current_interests = []
        players_names = [p.name for p in room.players]
        current_interests.append(f"all players in room: {','.join(players_names)}")
        disliked_players = []
        for p in room.players:
            if await self.alignment.is_opposing_alignment(self.name, p):
                disliked_players.append(p.name)
        current_interests.append(
            f"disliked players in room: {','.join(disliked_players)}"
        )
        self.logger.debug("exit")

    async def move(self, direction, world_state, isNpc=True):
        self.logger.debug("enter")
        self.logger.debug(f"{self.name} is moving {direction}")
        room = await world_state.get_room(self.room_id)
        room_id = [
            a
            for a in room.exits
            if a["direction"].name.lower() == direction["direction"].name.lower()
        ][0]
        if isNpc:
            self, world_state = await world_state.move_room_npc(
                room_id["id"], self, direction
            )
        else:
            self, world_state = await world_state.move_room_monster(
                room_id["id"], self, direction
            )

        self.logger.debug("exit")
        return self, world_state
