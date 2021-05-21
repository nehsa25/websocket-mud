from random import randint
from money import Money

class Monster:
    name = ""
    hitpoints = 0
    damage = None
    experience = 0
    money_potential = None
    money = []
    is_alive = True
    in_combat = None
    num_attack_targets = 1

    def __init__(self, name, hitpoints, damage_potential, experience, money_potential):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage_potential
        self.experience = experience
        self.money_potential = money_potential # (0, 100)

        # calculate money
        money = randint(money_potential[0], money_potential[1])
        coppers = []
        for i in range(money):
            coppers.append(Money.Coin.Copper)
        self.money = coppers

        # skeletons = 1
        # zombies = 100
        # ghouls = 1000


