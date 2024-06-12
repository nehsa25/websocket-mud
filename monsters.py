import random
from enum import Enum
from monster import Monster
from log_utils import LogUtils, Level


class Monsters:
    class MONSTERS(Enum):
        CRAB = 1
        SKELETON = 2
        ZOMBIE = 3
        ZOMBIE_SURFER = 4
        GHOUL = 5
        THUG = 6
        RAT = 7

    # used for respawning monsters
    async def get_monster(self, wanted_monster, room, logger):
        monster = None
        if wanted_monster == self.MONSTERS.CRAB:
            monster = self.get_crab()
            await monster.announce_entrance(room, logger)
        elif wanted_monster == self.MONSTERS.SKELETON:
            monster = self.get_skeleton()
            await monster.announce_entrance(room, logger)
        elif wanted_monster == self.MONSTERS.ZOMBIE:
            monster = self.get_zombie()
            await monster.announce_entrance(room, logger)
        elif wanted_monster == self.MONSTERS.ZOMBIE_SURFER:
            monster = self.get_zombie_surfer()
            await monster.announce_entrance(room, logger)
        elif wanted_monster == self.MONSTERS.GHOUL:
            monster = self.get_ghoul()
            await monster.announce_entrance(room, logger)
        elif wanted_monster == self.MONSTERS.THUG:
            monster = self.get_thug()
            await monster.announce_entrance(room, logger)
        elif wanted_monster == self.MONSTERS.RAT:
            monster = self.get_rat()
            await monster.announce_entrance(room, logger)

        LogUtils.debug(f'get_monster returning "{monster.name}"', logger)
        return monster

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
            death_cry=death_cry,
            entrance_cry=entrance_cry,
        )
