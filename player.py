import asyncio
import inspect
from random import randint
from alignment import Alignment
from items import Items
from log_utils import LogUtils
from mudevent import MudEvents
from stats import Stats
from utility import Utility

class Player(Utility):
    eye_color=None
    hair_color=None
    hair_length = None
    tattoes_placement=None
    tattoes_severity=None
    scars=None
    logger = None
    utility = None
    name = None
    location_id = 0
    pronoun = ""
    age = 0
    level = 0
    experience = 0
    race = None
    player_class = None
    stats = None
    in_combat = None
    weapon = Items.club
    ip = None
    inventory = None
    websocket = None
    rest_task =  None  # A resting task that check if this user is resting every 2 seconds
    mob_attack_task = None
    DEATH_RESPAWN_ROOM = 6
    room = None
    previous_room = None
    attack_task = None
    alignment = None
    
    def __init__(
        self,
        eye_color,
        hair_color,
        hair_length,
        tattoes_placement,
        tattoes_severity,
        scars,
        level,
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
        alignment = Utility.Alignment.NEUTRAL
    ):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Player() class", self.logger)
        self.eye_color = eye_color
        self.hair_color = hair_color
        self.hair_length = hair_length
        self.tattoes_placement = tattoes_placement
        self.tattoes_severity = tattoes_severity
        self.scars = scars
        self.name = name
        self.age = age
        self.level = level
        self.max_hitpoints = hp
        self.inventory = inventory
        self.location_id = location_id
        self.pronoun = pronoun
        self.race = race
        self.player_class = player_class
        self.ip = ip
        self.websocket = websocket

        # whether player is resting, poisoned, etc.
        self.stats = Stats(
            current_hp=hp,
            max_hp=hp,
            int=intelligence,
            faith=faith,
            agility=agility,
            perception=perception,
            determination=determination,
            strength=strength,
            logger=self.logger,
        )

        # if self.rest_task is None:
        #     self.rest_task = asyncio.create_task(self.check_resting())

        # if self.attack_task is None:
        #     self.attack_task = asyncio.create_task(self.check_combat())

        self.alignment = Alignment(Utility.Alignment.NEUTRAL, self.logger)

    async def can_telepath(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        return self.stats.intelligence > 10 and (self.race.telepathic or self.player_class.telepathic)
    
    # responsible for the "prepares to attack you messages"
    async def check_combat(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        battle = None
        while True:
            await asyncio.sleep(2)
            LogUtils.debug(f"{method_name}: {self.name} - checking combat", self.logger)

    async def get_player_hitpoint_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        hitpoint_status = ""
        if self.stats.current_hp <= 10:
            hitpoint_status = "frail"
        elif self.stats.current_hp >= 10 and self.stats.current_hp < 20:
            hitpoint_status = "weak"
        elif self.stats.current_hp >= 20 and self.stats.current_hp < 30:
            hitpoint_status = "average"
        elif self.stats.current_hp >= 30 and self.stats.current_hp < 40:
            hitpoint_status = "robust"
        elif self.stats.current_hp >= 40 and self.stats.current_hp < 50:
            hitpoint_status = "robust"
        elif self.stats.current_hp >= 50:
            hitpoint_status = "robust, healthy"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return hitpoint_status

    async def get_player_intelligence_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        intelligence = ""
        if self.stats.intelligence <= 10:
            intelligence = "dimwitted"
        elif self.stats.intelligence >= 10 and self.stats.intelligence < 20:
            intelligence = "slow"
        elif self.stats.intelligence >= 20 and self.stats.intelligence < 30:
            intelligence = "of average intelligence"
        elif self.stats.intelligence >= 30 and self.stats.intelligence < 40:
            intelligence = "smart"
        elif self.stats.intelligence >= 40 and self.stats.intelligence < 50:
            intelligence = "intelligent"
        elif self.stats.intelligence >= 50:
            intelligence = "genius"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return intelligence

    async def get_player_faith_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        faith = ""
        if self.stats.faith < 10:
            faith = "atheist"
        elif self.stats.faith > 10 and self.stats.intelligence <= 20:
            faith = "spiritual"
        elif self.stats.faith > 20 and self.stats.intelligence <= 30:
            faith = "highly spiritual"
        elif self.stats.faith > 30 and self.stats.intelligence <= 40:
            faith = "devout"
        elif self.stats.faith > 40 and self.stats.intelligence <= 50:
            faith = "holy"
        elif self.stats.faith > 50:
            faith = "godlike"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return faith

    async def get_player_strength_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        physique = ""
        if self.stats.strength < 10:
            physique = "puny"
        elif self.stats.strength >= 10 and self.stats.strength < 20:
            physique = "average"
        elif self.stats.strength >= 20 and self.stats.strength < 30:
            physique = "stout"
        elif self.stats.strength >= 30 and self.stats.strength < 40:
            physique = "solid"
        elif self.stats.strength >= 40 and self.stats.strength < 50:
            physique = "strong"
        elif self.stats.strength >= 50:
            physique = "godlike"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return physique

    async def get_player_health_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        health_status = ""
        hp_percent = self.max_hitpoints / self.stats.current_hp
        if self.stats.current_hp == self.max_hitpoints:
            health_status = "healthy"
        elif hp_percent > 0.2 and hp_percent <= 0.5:
            health_status = "severely wounded"
        elif hp_percent > 0.5 and hp_percent <= 0.8:
            health_status = "wounded"
        elif hp_percent >= 0.8:
            health_status = "slightly hurt"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return health_status

    async def get_player_agility_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        agility = ""
        if self.stats.agility <= 10:
            agility = "sluggish"
        elif self.stats.agility > 10 and self.stats.agility <= 20:
            agility = "slow"
        elif self.stats.agility > 20 and self.stats.agility <= 30:
            agility = "poorly coordinated"
        elif self.stats.agility > 30 and self.stats.agility <= 40:
            agility = "average"
        elif self.stats.agility > 40 and self.stats.agility <= 50:
            agility = "quick"
        elif self.stats.agility > 50:
            agility = "lightning fast"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return agility

    async def get_player_determination_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        determination = ""
        if self.stats.determination < 10:
            determination = "easily intimidated"
        elif self.stats.determination >= 10 and self.stats.determination < 20:
            determination = "nieve"
        elif self.stats.determination >= 20 and self.stats.determination < 30:
            determination = "focused"
        elif self.stats.determination >= 30 and self.stats.determination < 40:
            determination = "hyper-determined"
        elif self.stats.determination >= 40 and self.stats.determination < 50:
            determination = "hyper-determined"
        elif self.stats.determination >= 50:
            determination = "hyper-determined"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return determination

    async def get_player_perception_description(self, pronoun):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        perception = ""
        if self.stats.perception <= 10:
            perception = f"oblivious to {pronoun.value.possessive_pronoun} surroundings"
        elif self.stats.perception > 10 and self.stats.perception <= 20:
            perception = f"moderately aware of {pronoun.value.possessive_pronoun} surroundings"
        elif self.stats.perception > 20 and self.stats.perception <= 30:
            perception = f"actively aware of {pronoun.value.possessive_pronoun} surroundings"
        elif self.stats.perception > 30 and self.stats.perception <= 40:
            perception = f"keenly aware of everything around {pronoun.value.possessive_pronoun2}"
        elif self.stats.perception > 40 and self.stats.perception <= 50:
            perception = f"hyper-aware"
        elif self.stats.perception > 50:
            perception = f"vigilantly aware of everything around {pronoun.value.possessive_pronoun2}"
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return perception

    async def get_age(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        age = ""
        if self.age <= 20:
            age = "young"
        elif self.age > 20 and self.age <= 50:
            age = "seasoned"
        elif self.age > 50:
            age = "older"
        return age

    async def get_player_description(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        age = await self.get_age()
        sex = self.pronoun.value.sex
        hitpoint_status = await self.get_player_hitpoint_description()
        intelligence = await self.get_player_intelligence_description()
        physique = await self.get_player_strength_description()
        health_status = await self.get_player_health_description()
        agility = await self.get_player_agility_description()
        perception = await self.get_player_perception_description(self.pronoun)
        determination = await self.get_player_determination_description()
        faith = await self.get_player_faith_description()
        is_resting = "idly resting" if self.stats.is_resting else "not resting"
        
        msg = f"""
        {self.name} is a level {self.level}, {age} {sex} {self.race.name.capitalize()} {self.player_class.name.capitalize()}. {self.pronoun.value.pronoun.capitalize()} has {self.eye_color} eyes, {self.hair_length}, {self.hair_color} hair and is of {hitpoint_status} health.    
        {self.pronoun.value.pronoun.capitalize()} has a {physique} body and {self.pronoun.value.pronoun} moves with {agility} agility.  {self.name} appears {perception}, {intelligence}, {faith}, and {determination}.<br><br>    
        {self.name} appears to be {health_status} and is {is_resting}. Her mood is {self.stats.feriocity.name.lower()}."""
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return msg

    async def set_rest(self, rest: bool):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        if rest:
            self.send_message(
                MudEvents.RestEvent("You start resting.", is_resting=True),
                self.websocket,
            )
            self.stats.is_resting = True
        else:
            if self.stats.is_resting:
                self.stats.is_resting = False
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
    async def send_status(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        LogUtils.info(f"{method_name}: {self.name}: sending updated statuses", self.logger)
        name = self.name
        await self.send_message(
            MudEvents.HealthEvent(name, self.stats), self.websocket
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
        self.stats.current_hp = self.max_hitpoints
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
        LogUtils.info(f"{method_name}: {self.name}: sending updated inventory", self.logger)
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
            await asyncio.sleep(Utility.PLAYER_BASE_REST_WAIT_SECS)

            if self.stats.is_resting == True:
                LogUtils.debug("Checking if resting...", self.logger)
                if self.stats.current_hp < self.max_hitpoints:
                    heal = randint(1, 3)
                    if heal == 1:
                        await self.send_message(
                            MudEvents.InfoEvent(f"You recover {heal} hitpoint.")
                        )
                    else:
                        await self.send_message(
                            MudEvents.InfoEvent(f"You recover {heal} hitpoints.")
                        )
                    self.stats.current_hp += 3
                    if self.stats.current_hp >= self.max_hitpoints:
                        self.stats.current_hp = self.max_hitpoints
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
