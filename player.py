import asyncio
import inspect
from random import randint
from inventory import Inventory
from items import Items
from log_utils import LogUtils
from money import Money
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
    is_resting = False
    in_combat = None
    weapon = Items.club
    ip = None
    inventory = None
    websocket = None
    rest_task = (
        None  # A resting task that check if this user is resting every 2 seconds
    )
    mob_attack_task = None
    DEATH_RESPAWN_ROOM = 6
    room = None
    previous_room = None

    def __init__(
        self,
        name,
        hp,
        strength,
        agility,
        location_id,
        perception,
        inventory,
        ip,
        websocket,
        logger,
    ):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Player() class", self.logger)
        self.name = name
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.inventory = inventory
        self.location_id = location_id
        self.ip = ip
        self.websocket = websocket

        if self.rest_task is None:
            self.rest_task = asyncio.create_task(self.check_for_resting())

        # if self.mob_attack_task is None:
        #     self.mob_attack_task = asyncio.create_task(self.check_for_new_attacks())

    async def set_rest(self, rest: bool):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if rest:
            self.send_message(
                MudEvents.RestEvent("You start resting.", is_resting=True),
                self.websocket,
            )
            self.is_resting = True
        else:
            if self.is_resting:
                self.is_resting = False
                await self.send_message(
                    MudEvents.RestEvent("You are no longer resting.", is_resting=False),
                    self.websocket,
                )
            else:
                await self.send_message(
                    MudEvents.InfoEvent("You were not resting to begin with."),
                    self.websocket,
                )
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # shows color-coded health bar
    async def send_health(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        msg = f"{self.name}|{str(self.hitpoints)}/{str(self.max_hitpoints)}"
        await self.send_message(
            MudEvents.HealthEvent(msg, self.is_resting), self.websocket
        )
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # cancels all tasks and states you died if you die
    async def you_died(self, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # Your done boy.  Done.
        self.in_combat = False

        # state you died
        await self.send_message(MudEvents.InfoEvent("You died."), self.websocket)

        # alert others in the room where you died that you died..
        await self.room.alert(f"{self.name} died.", self.room, True, self)

        # drop all items
        for item in self.inventory:
            self.room.items.append(item)
        self.inventory = []

        # set player location to death respawn room
        player, world = await world.rooms.move_room(
            self.DEATH_RESPAWN_ROOM, self, world
        )

        # alert others in the room that new player has arrived
        await self.room.alert(
            f"A bright purple spark floods your vision.  When it clears, {self.name} is standing before you.  Naked.",
            player.room,
            True,
            self,
        )

        # set hits back to max / force health refresh
        self.hitpoints = self.max_hitpoints
        await self.send_health()

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player, world

    # break combat
    async def break_combat(self, rooms):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        self.in_combat = None
        self.room.alert(f"{self.name} stops fighting.", rooms[self.location_id])
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # shows inventory
    async def send_inventory(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await self.send_message(
            MudEvents.InventoryEvent(self.inventory),
            self.websocket,
        )
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # increases hp when resting
    async def check_for_resting(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(
            f"{method_name}: enter, checking if {self.name} is resting..", self.logger
        )

        while True:
            # Check resting every 2 seconds
            await asyncio.sleep(Utility.Share.PLAYER_BASE_REST_WAIT_SECS)

            if self.is_resting == True:
                LogUtils.debug("Checking if resting...", self.logger)
                if self.hitpoints < self.max_hitpoints:
                    heal = randint(1, 3)
                    if heal == 1:
                        await self.send_message(
                            MudEvents.InfoEvent(f"You recover {heal} hitpoint.")
                        )
                    else:
                        await self.send_message(
                            MudEvents.InfoEvent(f"You recover {heal} hitpoints.")
                        )
                    self.hitpoints += 3
                    if self.hitpoints >= self.max_hitpoints:
                        self.hitpoints = self.max_hitpoints
                        self.set_rest(False)
                        await self.send_message(
                            MudEvents.InfoEvent("You have fully recovered.")
                        )
                        await self.room.alert(
                            f"{self.name} appears to have fully recovered.",
                            exclude_player=True,
                            player=self,
                        )
                    await self.send_health()
