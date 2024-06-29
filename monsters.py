import asyncio
from enum import Enum
import inspect
import random
import time
from random import randint
from log_utils import LogUtils
from money import Money
from mudevent import MudEvents
from utility import Utility


class MonsterStats(Utility):
    name = ""
    hitpoints = 0
    damage = None
    experience = 0
    money = Money()
    is_alive = True
    in_combat = None
    players_seen = None
    num_attack_targets = None
    respawn_rate_secs = None
    dead_epoch = None
    death_cry = None
    entrance_cry = None
    victory_cry = None
    monster_type = None
    alignment = None
    wander = True
    wander_speed = 1  # 1 room / minute
    pronoun = "it"
    logger = None
    monster_wander_event = None
    last_exit = None
    respawn_rate_secs = 60 * 5


class Monster(Utility):
    class Alignment:
        GOOD = 1  # attacks evil players only
        NEUTRAL = 2  # only attacks if attacked
        EVIL = 3  # attacks good players only
        CHOATIC = 4  # attacks all players

    name = ""
    hitpoints = 0
    damage = None
    experience = 0
    money = Money()
    world = None
    is_alive = True
    in_combat = None
    players_seen = None
    num_attack_targets = None
    respawn_rate_secs = None
    dead_epoch = None
    death_cry = None
    entrance_cry = None
    monster_type = None
    alignment = None
    wander = True
    wander_speed = 1  # 1 room / minute
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

    def __init__(
        self,
        monster_name,
        hitpoints,
        damage,
        experience,
        money,
        death_cry,
        entrance_cry,
        victory_cry,
        monster_type,
        alignment,
        is_wanderer,
        wander_speed,
        pronoun,
        world,
        logger,
    ):

        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger

        LogUtils.debug(f"{method_name}: Initializing Monster() class", self.logger)
        self.hitpoints = hitpoints
        self.damage = damage
        self.experience = experience
        self.money = money
        self.death_cry = death_cry
        self.entrance_cry = entrance_cry
        self.victory_cry = victory_cry
        self.monster_type = monster_type
        self.alignment = alignment
        self.is_wanderer = is_wanderer
        self.wander_speed = wander_speed
        self.pronoun = pronoun
        self.logger = logger
        self.name = monster_name
        self.is_alive = True
        self.in_combat = None
        self.players_seen = []
        self.world = world

        LogUtils.info(
            f"[Monster] {monster_name} is created", self.logger
        )

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


class Monsters(Utility):
    class Monsters(Enum):
        SKELETON = 1
        ZOMBIE = 2
        ZOMBIE_SURFER = 3
        GHOUL = 4
        SHADE = 5

    class UndeadFactory:
        name = ""
        description = "Undead creatures that have been reanimated by dark magic. They are often found in graveyards and other places of death."
        font = "comic sans ms"
        font_size = 36
        log_utils = None

        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug("Initializing undead_factory() class", self.logger)
            self.logger = logger

        def get_monster(self, monster_type, worldstate):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)
            monster = None
            if monster_type == Monsters.Monsters.SKELETON:
                monster = self.Skeleton(worldstate, self.logger)
            LogUtils.debug(f"{method_name}: exit", self.logger)
            return monster

        class Skeleton(MonsterStats):
            logger = None
            possible_adjectives = ["Tottering", "Nasty", "Ravaged", "Rotting", "Dapper"]
            adjective_chance = 70
            instance = None

            def __init__(self, worldstate, logger):
                self.logger = logger
                LogUtils.debug("Initializing Skeleton() class", logger)
                self.name = "Skeleton"
                if random.randint(1, 100) < self.adjective_chance:
                    self.name = f"{random.choice(self.possible_adjectives)} Skeleton"
                self.death_cry = f"{self.name} falls over and dies.."
                self.entrance_cry = f"{self.name} wanders in.."
                self.victory_cry = (
                    "The skeleton gives an elegent bow before losing interest."
                )
                self.hitpoints = 10
                self.damage_potential = "1d4"
                self.experience = 100
                self.money = Money(randint(0, 10))

                # create new monster
                self.instance = Monster(
                    self.name,
                    self.hitpoints,
                    self.damage_potential,
                    self.experience,
                    self.money,
                    self.death_cry,
                    self.entrance_cry,
                    self.victory_cry,
                    Monsters.Monsters.SKELETON,
                    Monster.Alignment.NEUTRAL,
                    True,
                    1,
                    "it",
                    worldstate,
                    self.logger,
                )

        class Zombie:
            possible_adjectives = ["Decrepit", "Rotting", "Mad"]

            def __init__(self, room, worldstate, logger):
                self.logger = logger
                LogUtils.debug("Initializing Zombie() class", logger)
                self.name = f"Zombie"
                if random.random() < self.adjective_chance:
                    self.name = f"{random.choice(self.possible_adjectives)} Zombie"
                self.death_cry = f"{self.name} falls over and dies.."
                self.entrance_cry = f"{self.name} wanders in.."
                self.victory_cry = "The smiles sadly."
                self.hitpoints = 12
                self.damage_potential = "1d4"
                self.experience = 150
                self.money = Money(randint(0, 45))

        class ZombieSurfer:
            adjective_chance = 0.8
            possible_adjectives = [
                "Wasted",
                "Doddering",
                "Rotting",
                "Scarred",
                "Dirty",
                "Angry",
            ]

            def __init__(self, room, worldstate, logger):
                self.logger = logger
                LogUtils.debug("Initializing ZombieSurfer() class", logger)
                self.name = f"Zombie Surfer"
                if random.random() < self.adjective_chance:
                    self.name = (
                        f"{random.choice(self.possible_adjectives)} Zombie Surfer"
                    )
                self.death_cry = (
                    f'{self.name} says "Narley", then falls over and dies..'
                )
                self.entrance_cry = f"{self.name} wanders in.."
                self.victory_cry = (
                    "The zombie surfer stares at the corpse in confusion."
                )
                self.hitpoints = 15
                self.damage_potential = "1d6"
                self.experience = 175
                self.money = Money(randint(0, 50))

        class Ghoul:
            possible_adjectives = ["Gluttonous", "Scarred", "Ragged"]

            def __init__(self, room, worldstate, logger):
                self.logger = logger
                LogUtils.debug("Initializing Ghoul() class", logger)
                self.name = f"Ghoul"
                if random.random() < self.adjective_chance:
                    self.name = f"{random.choice(self.possible_adjectives)} Ghoul"
                self.death_cry = f"{self.name} falls over and dies.."
                self.entrance_cry = f"{self.name} wanders in.."
                self.victory_cry = "The ghoul makes no emotion."
                self.hitpoints = 15
                self.damage_potential = "1d6"
                self.experience = 175
                self.money = Money(randint(0, 75))

        class Shade:
            alignment = Monster.Alignment.NEUTRAL
            possible_adjectives = ["Ethereal", "Dark", "Menacing"]

            def __init__(self, room, worldstate, logger):
                self.logger = logger
                LogUtils.debug("Initializing Shade() class", logger)
                self.name = "Shade"
                if random.random() < self.adjective_chance:
                    self.name = f"{random.choice(self.possible_adjectives)} Share"
                self.death_cry = f"{self.name} sighs in relief and fades away.."
                self.entrance_cry = f"{self.name} floats in.."
                self.victory_cry = "The shade frowns slightly."
                self.hitpoints = 45
                self.damage_potential = "1d10"
                self.experience = 575
                self.money = Money(randint(0, 100))

    logger = None
    undead = None
    monsters = []

    def __init__(self, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Monsters() class", self.logger)
        self.undead = self.UndeadFactory(self.logger)
