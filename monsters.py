import random
from enum import Enum
from monster import Monster

class Monsters:
    class MONSTERS(Enum):
        CRAB = 1
        SKELETON = 2
        ZOMBIE = 3
        ZOMBIE_SURFER = 4
        GHOUL = 5
        THUG = 6

    # used for respawning monsters
    def get_monster(self, wanted_monster):
        if wanted_monster == self.MONSTERS.CRAB:
            return self.get_crab()
        elif wanted_monster == self.MONSTERS.SKELETON:
            return self.get_skeleton()
        elif wanted_monster == self.MONSTERS.ZOMBIE:
            return self.get_zombie()
        elif wanted_monster == self.MONSTERS.ZOMBIE_SURFER:
            return self.get_zombie_surfer()
        elif wanted_monster == self.MONSTERS.GHOUL:
            return self.get_ghoul()
        elif wanted_monster == self.MONSTERS.THUG:
            return self.get_thug()

    def get_crab(self):
        monsters = ['', '', '', '', '', '', '', '', 'Angry', 'Mad']
        name = f"{random.choice(monsters)} Giant Crab"
        death_cry = f"{name} scuttles one last time and dies.."
        entrance_cry = "Wanders in.."
        return Monster(
                        name=name.strip(),
                        monster_type=self.MONSTERS.CRAB,
                        hitpoints=12,
                        damage_potential='1d4',
                        experience=150,
                        money_potential=(0,100),
                        death_cry=death_cry,
                        entrance_cry=entrance_cry
                    )

    def get_skeleton(self):
        monsters = ['', '', '', '', '', '', '', '', 'Nasty', 'Ravaged', 'Rotting']
        name = f"{random.choice(monsters)} Skeleton"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = "Wanders in.."
        return Monster(
                        name=name.strip(),
                        monster_type=self.MONSTERS.CRAB,
                        hitpoints=10,
                        damage_potential='1d4',
                        experience=100,
                        money_potential=(0,10),
                        death_cry=death_cry,
                        entrance_cry=entrance_cry
                    )

    def get_zombie(self):
        monsters = ['', '', '', '', '', '', '', '', 'Rotting', 'Mad']
        name = f"{random.choice(monsters)} Zombie"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = "Wanders in.."
        return Monster(
                        name=name.strip(),
                        monster_type=self.MONSTERS.CRAB,
                        hitpoints=12,
                        damage_potential='1d4',
                        experience=150,
                        money_potential=(0,100),
                        death_cry=death_cry,
                        entrance_cry=entrance_cry
                    )

    def get_zombie_surfer(self):
        monsters = ['', '', '', '', '', '', '', 'Rotting', 'Scarred', 'Dirty', 'Angry']
        name = f"{random.choice(monsters)} Zombie Surfer"
        death_cry = f"{name} says \"Narley\", then falls over and dies.."
        entrance_cry = "Wanders in.."
        return Monster(
                        name=name.strip(),
                        monster_type=self.MONSTERS.CRAB,
                        hitpoints=15,
                        damage_potential='1d6',
                        experience=175,
                        money_potential=(0,1000),
                        death_cry=death_cry,
                        entrance_cry=entrance_cry
                    )

    def get_ghoul(self):
        monsters = ['', '', '', '', '', '', '', '', 'Gluttonous', 'Scarred', 'Ragged']
        name = f"{random.choice(monsters)} Ghoul"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = "Wanders in.."
        return Monster(
                        name=name.strip(),
                        monster_type=self.MONSTERS.GHOUL,
                        hitpoints=15,
                        damage_potential='1d6',
                        experience=175,
                        money_potential=(0,1000),
                        death_cry=death_cry,
                        entrance_cry=entrance_cry
                    )

    def get_thug(self):
        monsters = ['', '', '', '', '', '', '', '', 'Scarred', 'Dirty', 'Angry']
        name = f"{random.choice(monsters)} Thug"
        death_cry = f"{name} falls over and dies.."
        entrance_cry = "Wanders in.."
        return Monster(
                        name=name.strip(),
                        monster_type=self.MONSTERS.THUG,
                        hitpoints=15,
                        damage_potential='1d6',
                        experience=175,
                        money_potential= (0,1000),
                        death_cry=death_cry,
                        entrance_cry=entrance_cry
                    )
