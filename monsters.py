import random
from monster import Monster

class Monsters:    
    def get_crab():
        monsters = ['', '', '', '', '', '', '', '', 'Angry', 'Mad']
        name = f"{random.choice(monsters)} Giant Crab"
        return Monster(name.strip(), 12, '1d4', 150, (0,100))

    def get_skeleton():
        monsters = ['', '', '', '', '', '', '', '', 'Nasty', 'Ravaged', 'Rotting']
        name = f"{random.choice(monsters)} Skeleton"
        return Monster(name.strip(), 10, '1d4', 100, (0,1))

    def get_zombie():
        monsters = ['', '', '', '', '', '', '', '', 'Rotting', 'Mad']
        name = f"{random.choice(monsters)} Zombie"
        return Monster(name.strip(), 12, '1d4', 150, (0,100))

    def get_zombie_surfer():
        monsters = ['', '', '', '', '', '', '', 'Rotting', 'Scarred', 'Dirty', 'Angry']
        name = f"{random.choice(monsters)} Zombie Surfer"
        return Monster(name.strip(), 15, '1d6', 175, (0,1000))

    def get_ghoul():
        monsters = ['', '', '', '', '', '', '', '', 'Gluttonous', 'Scarred', 'Ragged']
        name = f"{random.choice(monsters)} Ghoul"
        return Monster(name.strip(), 15, '1d6', 175, (0,1000))

    def get_thug():
        monsters = ['', '', '', '', '', '', '', '', 'Scarred', 'Dirty', 'Angry']
        name = f"{random.choice(monsters)} Thug"
        return Monster(name.strip(), 15, '1d6', 175, (0,1000))


