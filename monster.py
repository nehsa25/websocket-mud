import time
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
    respawn_rate_secs = 60 # minute
    dead_epoch = None
    death_cry = None
    resurrect_cry = None

    def __init__(self, name, hitpoints, damage_potential, experience, money_potential, num_attack_targets = 1, respawn_rate_secs = 60, death_cry = None, resurrect_cry = None):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage_potential
        self.experience = experience
        self.money_potential = money_potential # tuple range (0, 100)
        self.num_attack_targets = num_attack_targets
        self.respawn_rate_secs = respawn_rate_secs
        self.death_cry = death_cry
        self.resurrect_cry = resurrect_cry

        # calculate money
        money = randint(money_potential[0], money_potential[1])
        coppers = []
        for i in range(money):
            coppers.append(Money.Coin.Copper)
        self.money = coppers

        # skeletons = 1
        # zombies = 100
        # ghouls = 1000

    def kill(self):
        self.is_alive = False
        self.dead_epoch = int(time.time())

        if self.death_cry != None:
            pass

    def resurrect(self):
        self.is_alive = True
        self.dead_epoch = None

        # PRONOUNCE YOU'VE ARISEN!
        if self.resurrect_cry != None:
            pass