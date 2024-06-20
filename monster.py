import inspect
import time
from random import randint
from log_utils import LogUtils
from money import Money
from mudevent import MudEvents
from utility import Utility

class Monster(Utility):
    name = ""
    hitpoints = 0
    damage = None
    experience = 0
    money_potential = None
    money = []
    is_alive = True
    in_combat = None
    players_seen = None
    num_attack_targets = None
    respawn_rate_secs = None
    dead_epoch = None
    death_cry = None
    entrance_cry = None
    monster_type = None
    pronoun = "it"
    logger = None
    def __init__(
        self,
        name,
        monster_type,
        hitpoints,
        damage_potential,
        experience,
        money_potential,
        death_cry,
        entrance_cry,
        victory_cry,
        logger,
        num_attack_targets=1,
        respawn_rate_secs=(30, 300),
    ):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage_potential
        self.experience = experience
        self.money_potential = money_potential  # tuple range (0, 100)
        self.num_attack_targets = num_attack_targets
        self.respawn_rate_secs = respawn_rate_secs
        self.death_cry = death_cry
        self.entrance_cry = entrance_cry
        self.monster_type = monster_type
        self.victory_cry = victory_cry
        self.logger = logger

        # calculate money
        money = randint(money_potential[0], money_potential[1])
        coppers = []
        for i in range(money):
            coppers.append(Money.Coin.Copper)
        self.money = coppers

        # calculate respawn_rate
        self.respawn_rate_secs = randint(respawn_rate_secs[0], respawn_rate_secs[1])

    # announce we're here!
    async def announce_entrance(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if self.entrance_cry != None:
            for player in room["players"]:
                await self.send_message(MudEvents.InfoEvent(self.entrance_cry), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def stop_combat(self, player):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await self.alert_room(self.victory_cry, player.room, True, player)
        self.in_combat = None
        await self.alert_room(f"{self.name} breaks off combat.", player.room, True, player)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        
    async def break_combat(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.in_combat = None
        await self.alert_room(f"{self.name} breaks off combat.", room, event_type=MudEvents.InfoEvent)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def kill(self, room, logger):
        self.is_alive = False
        self.dead_epoch = int(time.time())

        if self.death_cry != None:
            for player in room["players"]:
                await self.send_message(MudEvents.InfoEvent(self.death_cry), player.websocket)
                
