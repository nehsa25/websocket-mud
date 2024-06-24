import asyncio
import inspect
import random
import time
from random import randint
from log_utils import LogUtils
from money import Money
from mudevent import MudEvents
from utility import Utility


class Monster(Utility):
    class Alignment:
        GOOD = 1  # attacks evil players only
        NEUTRAL = 2  # only attacks if attacked
        EVIL = 3  # attacks good players only
        CHOATIC = 4  # attacks all players

    class Events:
        logger = None
        respawn_event = None

        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug("Initializing Monster.Events() class", self.logger)

        # respawn mobs after a certain amount of time
        async def respawn(self, rooms):
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", self.logger)

            while True:
                # Allow other tasks to complete
                await asyncio.sleep(2)

                # look through each room
                for room in rooms:
                    # and if the room has monsters
                    if len(room.monsters) > 0:
                        for monster in room.monsters:
                            # check if they're dead
                            if monster.is_alive == False:
                                current_epoch = int(time.time())

                                # if monster has been dead for more than monster.respawn_rate_secs, remove it and create new monster
                                # (we should consider making then kinda random (2-5 minutes for example))
                                secs_since_death = current_epoch - monster.dead_epoch
                                if secs_since_death >= monster.respawn_rate_secs:
                                    # remove old monster
                                    LogUtils.debug(
                                        f'Removing "{monster.name}" from room',
                                        self.logger,
                                    )
                                    room.monsters.remove(monster)

                                    # create new monster
                                    new_monster = await self.world.monsters.get_monster(
                                        monster.monster_type, room, self.logger
                                    )
                                    LogUtils.info(
                                        f'Respawning "{new_monster.name}" in room {room.id} ({room.name})',
                                        self.logger,
                                    )
                                    room.monsters.append(new_monster)

    events = None
    adjective_chance = 0.2  # the change that the monster will have an adjective like "rotting" or "nasty"
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
    monster_type = None
    alignment = None
    wander = True
    wander_speed = 1  # 1 room / minute
    pronoun = "it"
    logger = None
    monster_wander_event = None
    last_exit = None
    respawn_rate_secs = 60 * 5

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Monster() class", self.logger)

        if self.events is None:
            self.events = Monster.Events(self.logger)

    # async def wander(self):
    #     exit_option = random.choice(self.room.exits)
    #     while self.last_exit == exit_option or len(self.room.exits) == 1:
    #         exit_option = random.choice(self.room.exits)

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


class Monsters(Monster):

    class undead_factory(Monster):
        name = ""
        description = "Undead creatures that have been reanimated by dark magic. They are often found in graveyards and other places of death."
        font = "comic sans ms"
        font_size = 36
        log_utils = None

        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug("Initializing undead_factory() class", self.logger)
            self.logger = logger

        class Skeleton(Monster):
            logger = None
            possible_adjectives = ["Tottering", "Nasty", "Ravaged", "Rotting", "Dapper"]

            def __init__(self, logger):
                self.logger = logger
                LogUtils.debug("Initializing Skeleton() class", logger)
                self.name = "Skeleton"
                if random.random() < self.adjective_chance:
                    self.name = f"{random.choice(self.possible_adjectives)} Skeleton"
                self.death_cry = f"{self.name} falls over and dies.."
                self.entrance_cry = f"{self.name} wanders in.."
                self.victory_cry = "The skeleton gives an elegent bow."
                self.hitpoints = 10
                self.damage_potential = "1d4"
                self.experience = 100
                self.money.coppers = randint(0, 10)

        class Zombie(Monster):
            possible_adjectives = ["Decrepit", "Rotting", "Mad"]

            def __init__(self, logger):
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
                for i in range(randint(0, 25)):
                    self.money.coppers.append(Money.Coin.Copper)

        class ZombieSurfer(Monster):
            adjective_chance = 0.8
            possible_adjectives = [
                "Wasted",
                "Doddering",
                "Rotting",
                "Scarred",
                "Dirty",
                "Angry",
            ]

            def __init__(self, logger):
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
                for i in range(randint(0, 25)):
                    self.money.coppers.append(Money.Coin.Copper)

        class Ghoul(Monster):
            possible_adjectives = ["Gluttonous", "Scarred", "Ragged"]

            def __init__(self, logger):
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
                for i in range(randint(0, 30)):
                    self.money.coppers.append(Money.Coin.Copper)

        class Shade(Monster):
            alignment = Monster.Alignment.NEUTRAL
            possible_adjectives = ["Ethereal", "Dark", "Menacing"]

            def __init__(self, logger):
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
                for i in range(randint(0, 50)):
                    self.money.coppers.append(Money.Coin.Copper)

    logger = None

    undead = None

    def __init__(self, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Monsters() class", self.logger)
        self.undead = self.undead_factory(self.logger)
