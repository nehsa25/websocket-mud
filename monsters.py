import asyncio
import inspect
import random
from enum import Enum
import time
from monster import Monster
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility


class Monsters(Utility):
    logger = None
    mob_attack_task = None

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Monsters() class", self.logger)

    class MONSTERS(Enum):
        CRAB = 1
        SKELETON = 2
        ZOMBIE = 3
        ZOMBIE_SURFER = 4
        GHOUL = 5
        THUG = 6
        RAT = 7

    # used for respawning monsters
    async def get_monster(self, wanted_monster, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        monster = None
        if wanted_monster == self.MONSTERS.CRAB:
            monster = self.get_crab()
            await monster.announce_entrance(room, self.logger)
        elif wanted_monster == self.MONSTERS.SKELETON:
            monster = self.get_skeleton()
            await monster.announce_entrance(room, self.logger)
        elif wanted_monster == self.MONSTERS.ZOMBIE:
            monster = self.get_zombie()
            await monster.announce_entrance(room, self.logger)
        elif wanted_monster == self.MONSTERS.ZOMBIE_SURFER:
            monster = self.get_zombie_surfer()
            await monster.announce_entrance(room, self.logger)
        elif wanted_monster == self.MONSTERS.GHOUL:
            monster = self.get_ghoul()
            await monster.announce_entrance(room, self.logger)
        elif wanted_monster == self.MONSTERS.THUG:
            monster = self.get_thug()
            await monster.announce_entrance(room, self.logger)
        elif wanted_monster == self.MONSTERS.RAT:
            monster = self.get_rat()
            await monster.announce_entrance(room, self.logger)

        LogUtils.debug(f'get_monster returning "{monster.name}"', self.logger)
        return monster

    # respawn mobs after a certain amount of time
    async def respawn_mobs(self, rooms):
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
                                    f'Removing "{monster.name}" from room', self.logger
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

    # # main loop for checking if monsters are attacking you
    # async def mob_combat(self):
    #     method_name = inspect.currentframe().f_code.co_name
    #     LogUtils.debug(f"{method_name}: enter", self.logger)

    #     # sleep delay between rounds
    #     LogUtils.debug(
    #         f"{method_name}: Sleeping {str(self.COMBAT_WAIT_SECS)} seconds",
    #         self.logger,
    #     )
    #     await asyncio.sleep(self.COMBAT_WAIT_SECS)

    #     for player in self.world.players.players:
    #         LogUtils.debug(
    #             f'{method_name}: On player "{player.name}", Running loop2...',
    #             self.logger,
    #         )

    #         # we need to get room again after we've slept
    #         room = await self.world.get_room(player.location_id, self.logger)

    #         # calculcate round damanage
    #         await self.apply_mob_round_damage(self.player, room)

    def get_rat(self):
        monsters = ["", "", "", "", "", "", "festering", "Maddened", "Angry", "Filthy"]
        name = f"{random.choice(monsters)} Brown Rat"
        death_cry = f"{name} spasms in agony, then is still."
        entrance_cry = f"{name} scurries in.."
        return Monster(
            name=name.strip(),
            monster_type=self.MONSTERS.CRAB,
            hitpoints=10,
            damage_potential="1d3",
            experience=40,
            money_potential=(0, 0),
            logger=self.logger,
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )

    def get_crab(self):
        monsters = ["", "", "", "", "", "", "", "", "Angry", "Mad"]
        name = f"{random.choice(monsters)} Giant Crab"
        death_cry = f"{name} kicks one last time and dies.."
        entrance_cry = f"{name} scuttles in.."
        return Monster(
            name=name.strip(),
            monster_type=self.MONSTERS.CRAB,
            hitpoints=50,
            damage_potential="1d4",
            experience=150,
            money_potential=(0, 100),
            logger=self.logger,
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )

    def get_skeleton(self):
        monsters = [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Tottering",
            "Nasty",
            "Ravaged",
            "Rotting",
        ]
        name = f"{random.choice(monsters)} Skeleton"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = f"{name} wanders in.."
        return Monster(
            name=name.strip(),
            monster_type=self.MONSTERS.SKELETON,
            hitpoints=10,
            damage_potential="1d4",
            experience=100,
            money_potential=(0, 10),
            logger=self.logger,
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )

    def get_zombie(self):
        monsters = ["", "", "", "", "", "", "", "Decrepit", "Rotting", "Mad"]
        name = f"{random.choice(monsters)} Zombie"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = f"{name} wanders in.."
        return Monster(
            name=name.strip(),
            monster_type=self.MONSTERS.ZOMBIE,
            hitpoints=12,
            damage_potential="1d4",
            experience=150,
            money_potential=(0, 100),
            logger=self.logger,
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )

    def get_zombie_surfer(self):
        monsters = [
            "",
            "",
            "",
            "",
            "",
            "Wasted",
            "Doddering",
            "Rotting",
            "Scarred",
            "Dirty",
            "Angry",
        ]
        name = f"{random.choice(monsters)} Zombie Surfer"
        death_cry = f'{name} says "Narley", then falls over and dies..'
        entrance_cry = f"{name} wanders in.."
        return Monster(
            name=name.strip(),
            monster_type=self.MONSTERS.ZOMBIE_SURFER,
            hitpoints=15,
            damage_potential="1d6",
            experience=175,
            money_potential=(0, 1000),
            logger=self.logger,
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )

    def get_ghoul(self):
        monsters = ["", "", "", "", "", "", "", "", "Gluttonous", "Scarred", "Ragged"]
        name = f"{random.choice(monsters)} Ghoul"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = f"{name} wanders in.."
        return Monster(
            name=name.strip(),
            monster_type=self.MONSTERS.GHOUL,
            hitpoints=15,
            damage_potential="1d6",
            experience=175,
            money_potential=(0, 1000),
            logger=self.logger,
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )

    def get_thug(self):
        monsters = ["", "", "", "", "", "", "", "", "Scarred", "Dirty", "Angry"]
        name = f"{random.choice(monsters)} Thug"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = f"{name} saunders in.."
        return Monster(
            name=name.strip(),
            monster_type=self.MONSTERS.THUG,
            hitpoints=15,
            damage_potential="1d6",
            experience=175,
            money_potential=(0, 1000),
            logger=self.logger,
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )
