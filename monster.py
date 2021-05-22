import time
from random import randint
from money import Money
from utility import Utility

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
    entrance_cry = None
    monster_type = None

    def __init__(self, name, monster_type, hitpoints, damage_potential, 
                experience, money_potential, death_cry, entrance_cry,
                num_attack_targets = 1, respawn_rate_secs = 60):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage_potential
        self.experience = experience
        self.money_potential = money_potential # tuple range (0, 100)
        self.num_attack_targets = num_attack_targets
        self.respawn_rate_secs = respawn_rate_secs
        self.death_cry = death_cry
        self.entrance_cry = entrance_cry
        self.monster_type = monster_type

        # calculate money
        money = randint(money_potential[0], money_potential[1])
        coppers = []
        for i in range(money):
            coppers.append(Money.Coin.Copper)
        self.money = coppers

    # announce we're here!
    async def announce_entrance(self, room, logger):        
        if self.entrance_cry != None:
            for player in room['players']:
                await Utility.send_msg(self.entrance_cry, 'info', player.websocket, logger)

    async def kill(self, room, logger):
        self.is_alive = False
        self.dead_epoch = int(time.time())

        if self.death_cry != None:
            for player in room['players']:
                await Utility.send_msg(self.death_cry, 'info', player.websocket, logger)
