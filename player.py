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
    faith = 0
    age = 0
    intelligence = 0
    hitpoints = 0
    max_hitpoints = 0
    location_id = 0
    pronoun = ""
    strength = 0
    agility = 0
    perception = 0
    determination = 0
    experience = 0
    race = ""
    player_class = ""
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
        intelligence,
        faith,
        pronoun,
        race,
        determination,
        player_class,
        strength,
        agility,
        location_id,
        perception,
        inventory,
        age,
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
        self.faith = faith
        self.intelligence = intelligence
        self.pronoun = pronoun
        self.race = race
        self.age = age
        self.player_class = player_class
        self.ip = ip
        self.websocket = websocket
        self.determination = determination
        if self.rest_task is None:
            self.rest_task = asyncio.create_task(self.check_for_resting())

        # if self.mob_attack_task is None:
        #     self.mob_attack_task = asyncio.create_task(self.check_for_new_attacks())


    async def get_player_hitpoint_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        hitpoint_status = ""
        if self.hitpoints < 10:
            hitpoint_status = "frail"
        elif self.hitpoints > 10 and self.hitpoints <= 20:
            hitpoint_status = "weak"
        elif self.hitpoints > 20 and self.hitpoints <= 30:
            hitpoint_status = "average"
        elif self.hitpoints > 30 and self.hitpoints <= 40:
            hitpoint_status = "robust"
        elif self.hitpoints > 40 and self.hitpoints <= 50:
            hitpoint_status = "robust"
        elif self.hitpoints > 50:
            hitpoint_status = "robust, healthy"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return hitpoint_status

    async def get_player_intelligence_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        intelligence = ""
        if self.intelligence < 10:
            intelligence = "dimwitted"
        elif self.intelligence > 10 and self.intelligence <= 20:
            intelligence = "slow"
        elif self.intelligence > 20 and self.intelligence <= 30:
            intelligence = "average"
        elif self.intelligence > 30 and self.intelligence <= 40:
            intelligence = "smart"
        elif self.intelligence > 40 and self.intelligence <= 50:
            intelligence = "intelligent"
        elif self.intelligence > 50:
            intelligence = "genius"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return intelligence

    async def get_player_strength_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        physique = ""
        if self.strength < 10:
            physique = "punily"
        elif self.strength > 10 and self.strength <= 20:
            physique = "average"
        elif self.strength > 20 and self.strength <= 30:
            physique = "stout"
        elif self.strength > 30 and self.strength <= 40:
            physique = "solid"
        elif self.strength > 40 and self.strength <= 50:
            physique = "strong"
        elif self.strength > 50:
            physique = "godlike"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return physique

    async def get_player_health_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        health_status = ""
        hp_percent = self.max_hitpoints / self.hitpoints
        if self.hitpoints == self.max_hitpoints:
            health_status = "healthy"
        elif hp_percent > .2 and hp_percent <= .5:
            health_status = "severely wounded"
        elif hp_percent > .5 and hp_percent <= .8:
            health_status = "wounded"
        elif hp_percent >= .8:
            health_status = "slightly hurt"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return health_status

    async def get_player_agility_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        agility = ""
        if self.agility < 10:
            agility = "sluggish"
        elif self.agility > 10 and self.agility <= 20:
            agility = "slow"
        elif self.agility > 20 and self.agility <= 30:
            agility = "poorly coordinated"
        elif self.agility > 30 and self.agility <= 40:
            agility = "average"
        elif self.agility > 40 and self.agility <= 50:
            agility = "quick"
        elif self.agility > 50:
            agility = "lightning fast"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return agility

    async def get_player_determination_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        determination = ""
        if self.determination < 10:
            determination = "easily intimidated"
        elif self.determination > 10 and self.determination <= 20:
            determination = "nieve"
        elif self.determination > 20 and self.determination <= 30:
            determination = "focused"
        elif self.determination > 30 and self.determination <= 40:
            determination = "hyper focused"
        elif self.determination > 40 and self.determination <= 50:
            determination = "hyper focused"
        elif self.determination > 50:
            determination = "hyper focused"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return determination

    async def get_player_perception_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        perception = ""
        if self.perception < 10:
            perception = "oblivious to their surroundings."
        elif self.perception > 10 and self.perception <= 20:
            perception = "moderately aware of their surroundings"
        elif self.perception > 20 and self.perception <= 30:
            perception = "actively aware of their surroundings"
        elif self.perception > 30 and self.perception <= 40:
            perception = "keenly aware of everything around them"
        elif self.perception > 40 and self.perception <= 50:
            perception = "hyper aware"
        elif self.perception > 50:
            perception = "vigilantly aware of everything around them"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return perception

    async def get_sex(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        sex = ""
        if self.pronoun == "he":
            sex = "male"
        elif self.pronoun == "she":
            sex = "female"
        elif self.pronoun == "it":
            sex = "it"            
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return sex

    async def get_age(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        age = ""
        if self.age <= 20:
            age = "young"
        elif self.age > 20 and self.age <= 50:
            age = "middle aged"
        elif self.age > 50:
            age = "old"
        return age

    async def get_player_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        age = await self.get_age()
        sex = await self.get_sex()
        hitpoint_status = await self.get_player_hitpoint_description()
        intelligence = await self.get_player_intelligence_description()
        physique = await self.get_player_strength_description()
        health_status = await self.get_player_health_description()
        agility = await self.get_player_agility_description()
        perception = await self.get_player_perception_description()
        determination = await self.get_player_determination_description()
        is_resting = "idly resting" if self.is_resting else "not resting"            
        return f"""
    
    {self.name} is a level {self.level}, {age} {sex} {self.race.name.capitalize()} {self.player_class.lower()} of {hitpoint_status} appearance. 
    
    {self.pronoun.capitalize()} has a {physique} body build and moves with {agility} agility.  {self.name} appears {perception}, {intelligence}, and {determination}. 
    
    {self.name} appears to be {health_status} and is {is_resting}."""

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
