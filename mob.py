import asyncio
import inspect
import random
import time
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility


class Mob(Utility):
    name = ""
    hitpoints = 0
    damage = None
    experience = 0
    money = None
    world = None
    is_alive = True
    in_combat = None
    players_seen = None
    num_attack_targets = None
    pronoun = "it"
    logger = None
    monster_wander_event = None
    last_exit = None
    respawn_rate_secs = 60 * 5
    respawn_event = None
    check_combat_event = None
    wander_event = None
    last_exit = None
    wander_loop = None
    respawn_loop = None
    check_combat_loop = None
    room = None
    previous_room = None
    death_cry = ""
    entrance_cry = ""
    victory_cry = ""
    damage_potential = ""
    allowed_in_city = False

    # announce we're here!
    async def announce_entrance(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if self.entrance_cry != None:
            for player in room["players"]:
                await self.send_message(
                    MudEvents.InfoEvent(self.entrance_cry), player.websocket
                )
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def stop_combat(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await self.alert_room(self.victory_cry, player.room, True, player)
        self.in_combat = None
        await self.alert_room(
            f"{self.name} breaks off combat.", player.room, True, player
        )
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def break_combat(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.in_combat = None
        await self.alert_room(
            f"{self.name} breaks off combat.", room, event_type=MudEvents.InfoEvent
        )
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def kill(self, room, logger):
        self.is_alive = False
        self.dead_epoch = int(time.time())

        if self.death_cry != None:
            for player in room["players"]:
                await self.send_message(
                    MudEvents.InfoEvent(self.death_cry), player.websocket
                )

    async def check_for_combat(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.info(f"{self.name} checking for combat", self.logger)

    # respawn mobs after a certain amount of time
    async def respawn(self, world_state):
        LogUtils.info(f"{self.name} checking for respawn: {world_state}", self.logger)

        # # look through each room
        # for room in rooms:
        #     # and if the room has monsters
        #     if len(room.monsters) > 0:
        #         for monster in room.monsters:
        #             # check if they're dead
        #             if monster.is_alive == False:
        #                 current_epoch = int(time.time())

        #                 # if monster has been dead for more than monster.respawn_rate_secs, remove it and create new monster
        #                 # (we should consider making then kinda random (2-5 minutes for example))
        #                 secs_since_death = current_epoch - monster.dead_epoch
        #                 if secs_since_death >= monster.respawn_rate_secs:
        #                     # remove old monster
        #                     LogUtils.debug(
        #                         f'Removing "{monster.name}" from room',
        #                         self.logger,
        #                     )
        #                     room.monsters.remove(monster)

        #                     # create new monster
        #                     new_monster = await self.world.monsters.get_monster(
        #                         monster.monster_type, room, self.logger
        #                     )
        #                     LogUtils.info(
        #                         f'Respawning "{new_monster.name}" in room {room.id} ({room.name})',
        #                         self.logger,
        #                     )
        #                     room.monsters.append(new_monster)

    async def wander(self, world_state):
        LogUtils.info(f"{self.name} checking for wander", self.logger)
        last_position = None
        while True:
            await asyncio.sleep(self.wander_speed)
            will_travel = False
            max_num_attempts = len(self.room.exits)
            current_attempt = 1
            while not will_travel:
                potential_room = random.choice(self.room.exits)
                if potential_room != self.last_exit:
                    will_travel = True
                    self.previous_room = self.room
                    self.room, self.world = world_state.move_room_monster(
                        potential_room.id, self)
                    LogUtils.debug(
                        f"{self.name} wanders {potential_room} from room {last_position} to {self.room.id}",
                        self.logger,
                    )
                    break
                current_attempt += 1
                if current_attempt >= max_num_attempts:
                    break
