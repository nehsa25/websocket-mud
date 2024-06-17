import asyncio
import inspect
from random import randint
import random
from items import Items
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Player(Utility):
    logger = None
    utility = None
    name = None
    level = 1
    hitpoints = 0
    max_hitpoints = 0
    location_id = 0
    strength = 0
    agility = 0
    perception = 0
    experience = 0
    resting = False
    in_combat = None
    ip = None
    inventory = [Items.book, Items.cloth_pants]
    money = []
    websocket = None
    rest_task = None # A resting task that check if this user is resting every 2 seconds
    mob_attack_task = None

    def __init__(
        self,
        name,
        hp,
        strength,
        agility,
        location_id,
        perception,
        ip,
        websocket,
        logger,
    ):
        self.logger = logger
        LogUtils.debug(f"Initializing Player() class", self.logger)
        if self.utility is None:
            self.utility = Utility(logger)
        self.name = name
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.location_id = location_id
        self.ip = ip
        self.websocket = websocket
        if self.rest_task is None:
            self.rest_task = asyncio.create_task(self.check_for_resting())

    # shows color-coded health bar
    async def show_health(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        msg = f"{self.name}|{str(self.hitpoints)}/{str(self.max_hitpoints)}"
        if self.resting:
            msg += "|REST"
        await self.utility.send_message(MudEvents.HealthEvent(msg), self.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # cancels all tasks and states you died if you die
    async def you_died(self):
        # set combat to false
        self.in_combat = False

        # state you died
        await self.send_message(MudEvents.InfoEvent("You died."))

        # alert others in the room where you died that you died..
        room = await self.world.get_room(self.location_id)
        for p in room.players:
            if p != self:
                await self.send_message(MudEvents.InfoEvent(f"{self.name} died."), p.websocket)

        # drop all items
        room = await self.world.get_room(self.location_id)
        for item in self.inventory:
            room.items.append(item)
        self.inventory = []

        # set player location to beach shore
        self.player, self.world = await self.world.move_room(
            self.DEATH_RESPAWN_ROOM, self.player, self.world
        )

        # alert others in the room that new player has arrived
        room = await self.world.get_room(self.DEATH_RESPAWN_ROOM, self.logger)
        for p in room.players:
            if p != self:
                await self.send_message(MudEvents.InfoEvent(f"A bright purple spark floods your vision.  When it clears, {self.name} is standing before you.  Naked."), p.websocket)

        # set hits back to max / force health refresh
        self.hitpoints = self.max_hitpoints
        await self.show_health()

    # Determines round damage for each player
    async def apply_mob_round_damage(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # determine damage
        total_damage = await self.calculate_mob_damage(self.player, room)

        # update hp
        if total_damage > 0:
            self.hitpoints = self.hitpoints - total_damage

            # no point in continuing if player is dead..
            if self.hitpoints <= 0:
                await self.you_died()

            # Updating health bar
            await self.show_health()

        LogUtils.debug(f"{method_name}: exit", self.logger)

    # break combat
    async def break_combat(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.in_combat = None        
        self.alert_room(self.world, f"{self.name} stops fighting.")        
        LogUtils.debug(f"{method_name}: exit", self.logger)
        
    # stops resting
    async def stops_resting(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.resting = False
        await self.send_message(MudEvents.InfoEvent("You are no longer resting."))  
        self.alert_room(self.world, f"{self.name} stirs and stops resting.")        
        LogUtils.debug(f"{method_name}: exit", self.logger)
        
    # shows inventory
    async def show_inventory(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        items = []
        for item in self.inventory:
            items.append(item.name)
        inv_event = MudEvents.InventoryEvent(items)
        await self.utility.send_message(inv_event, self.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # increases hp when resting
    async def check_for_resting(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, checking if {self.name} is resting..", self.logger)

        while True:
            # Check resting every 2 seconds
            await asyncio.sleep(self.REST_WAIT_SECS)

            if self.resting == True:
                LogUtils.debug("Checking if resting...", self.logger)
                if self.hitpoints < self.max_hitpoints:
                    heal = randint(1, 3)
                    if heal == 1:
                        await self.send_message(MudEvents.InfoEvent(f"You recover {heal} hitpoint."))
                    else:
                        await self.send_message(MudEvents.InfoEvent(f"You recover {heal} hitpoints."))
                    self.hitpoints += 3
                    if self.hitpoints >= self.max_hitpoints:
                        self.hitpoints = self.max_hitpoints
                        self.resting = False
                        await self.send_message(MudEvents.InfoEvent("You have fully recovered."))
                        await self.alert_room(self.world, f"{self.name} appears to have fully recovered.")
                    await self.show_health()

    # responsible for the "prepares to attack you messages"
    async def check_for_new_attacks(self, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        # for each monster in room still alive
        for monster in room.monsters:
            if monster.is_alive == True:
                LogUtils.debug(
                    f'{method_name}: Monster "{monster.name}" is alive', logger
                )

                # choose a player to attack each round
                current_combat = monster.in_combat

                if (
                    monster.in_combat == None
                ):  # if monster is not attacking anyone, just pick someone
                    monster.in_combat = random.choice(room.players)
                    LogUtils.debug(
                        f'{method_name}: "{monster.name}" is not attacking anyone.  Now attacking {monster.in_combat.name}',
                        self.logger,
                    )
                elif (
                    monster.players_seen != room.players
                ):  # change combat if players enter/leave room
                    prev_combat = monster.in_combat
                    monster.in_combat = random.choice(room.players)
                    monster.players_seen = room.players.copy()
                    LogUtils.debug(
                        f'{method_name}: The players changed in room "{room.name}".  "{monster.name}" was attacking {prev_combat.name}, now attacking: {monster.in_combat.name}',
                        self.logger,
                    )
                else:
                    LogUtils.debug(
                        f"{method_name}: Monster ({monster.name}) is in combat and nothing has changed in the room to switch combat...",
                        self.logger,
                    )

                # if the mob changed combat state, send message
                if monster.in_combat != current_combat:
                    LogUtils.debug(
                        f"{method_name}: Monster is changing combat: {monster.name}",
                        self.logger,
                    )

                    # cycle through all players
                    for p in room.players:
                        if monster.in_combat == p:
                            await self.send_message(MudEvents.AttackEvent(f"{monster.name} positions to attack you."), p.websocket)
                            
                            # stop resting
                            if p.resting == True:
                                p.resting = False
                                await self.send_message(MudEvents.InfoEvent("You are no longer resting."), p.websocket)

                            for p2 in room.players:
                                if monster.in_combat != p2:
                                    await self.send_message(MudEvents.InfoEvent(f"{monster.name} prepares to attack {p.name}!"), p2.websocket)

                            # break out of loop
                            LogUtils.debug(
                                f"{method_name}: Breaking out of loop1", self.logger
                            )
                            break
        LogUtils.debug(f"{method_name}: exit", self.logger)
