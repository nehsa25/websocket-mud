import random
from monster import Monster

class Monsters:    
    def get_skeleton():
        monsters = ['', 'Nasty', 'Smelly', 'Rotting']
        name = f"{random.choice(monsters)} Skeleton"
        return Monster(name.strip(), 10, '1d4', 100)

    def get_zombie():
        monsters = ['', 'Armless', 'Rotting', 'Mad']
        name = f"{random.choice(monsters)} Zombie"
        return Monster(name.strip(), 12, '1d4', 150)

    def get_ghoul():
        monsters = ['', 'Angry', 'Wilted', 'Ragged']
        name = f"{random.choice(monsters)} Ghoul"
        return Monster(name.strip(), 15, '1d6', 175)
