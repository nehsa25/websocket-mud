from __future__ import annotations
import asyncio
from random import randint
from typing import Dict

from core.data.attributes_data import AttributesData
from core.data.room_data import RoomData
from core.enums.alignments import AlignmentEnum
from core.enums.body_types import BodyTypesEnum
from core.enums.eye_brows import EyeBrowEnum
from core.enums.eye_colors import EyeColorEnum
from core.enums.facial_hair import FacialHairEnum
from core.enums.hair_colors import HairColorEnum
from core.enums.hair_styles import HairStylesEnum
from core.enums.player_classes import PlayerClassEnum
from core.enums.races import PlayerRaceEnum
from core.enums.rooms import RoomEnum
from core.enums.send_scope import SendScopeEnum
from core.enums.sex import SexEnum
from core.events.info import InfoEvent
from core.events.inventory import InventoryEvent
from core.events.rest import RestEvent
from core.interfaces.character import CharacterInterface
from core.interfaces.mob import MOBInterface
from settings.world_settings import WorldSettings
from utilities.log_telemetry import LogTelemetryUtility


class CharacterData(CharacterInterface, MOBInterface):
    logger = None

    def __init__(
            self,
                firstname: str = "",
                lastname: str = "",
                experience: int = 0,
                level: int = 1,
                money: int = 0,
                sex: str = "",
                attributes={},
                alignment: str = AlignmentEnum.NEUTRAL.value,
                player_race: str = PlayerRaceEnum.HUMAN.value,
                player_class: str = PlayerClassEnum.WARRIOR.value,
                eye_brow: str = EyeBrowEnum.BUSHY.value,
                eye_color: str = EyeColorEnum.BROWN.value,
                body_type: str = BodyTypesEnum.AVERAGE.value,
                facial_hair: str = FacialHairEnum.NONE.value,
                hair_color: str = HairColorEnum.BROWN.value,
                hair_style: str = HairStylesEnum.SHORTHAIR.value,
                room_id: int = RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                room: "RoomData" = None
    ):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing CharacterData")
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.experience: int = experience
        self.level: int = level
        self.money: int = money        
        self.room = room
        self.room_id: int = room_id

        if sex == "":
            self.sex: str = SexEnum.MALE
        else:
            self.sex = sex

        self.eye_color: str = eye_color
        self.eye_brow: str = eye_brow
        self.body_type: str = body_type
        self.hair_color: str = hair_color
        self.hair_style: str = hair_style

        if attributes == {}:
            self.attributes = (
                AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
            )
        else:
            self.attributes = attributes

        self.alignment: str = alignment
        self.player_race: str = player_race
        self.player_class: str = player_class
        self.facial_hair: str = facial_hair

    def __str__(self):
        return f"Character(name={self.name}, level={self.level}, experience={self.experience}, money={self.money}"

    @property
    def name(self) -> str:
        return f"{self.firstname} {self.lastname}"

    def to_dict(self) -> Dict:
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "experience": self.experience,
            "level": self.level,
            "money": self.money,
            "sex": self.sex,
            "attributes": self.attributes.to_dict(),
            "alignment": self.alignment,
            "player_race": self.player_race,
            "player_class": self.player_class,
            "room_id": self.room_id,
            "eye_color": self.eye_color,
            "eye_brow": self.eye_brow,
            "body_type": self.body_type,
            "hair_color": self.hair_color,
            "hair_style": self.hair_style,
        }

    async def check_combat(self, room):
        pass

    async def break_combat(self, room):
        pass

    async def attack(self, room):
        pass

    async def speak(self, room):
        pass

    async def move(self, direction, isNpc=True):
        pass

    async def get_hp(self, room):
        pass

    async def get_hp_description(self):
        self.logger.debug("enter")
        health_status = ""
        hp_percent = self.max_hp / self.statuses.current_hp
        if self.statuses.current_hp == self.max_hp:
            health_status = "healthy"
        elif 0.2 < hp_percent <= 0.5:
            health_status = "severely wounded"
        elif 0.5 < hp_percent <= 0.8:
            health_status = "wounded"
        elif hp_percent >= 0.8:
            health_status = "slightly hurt"
        self.logger.debug("exit")
        return health_status

    async def get_intelligence(self):
        pass

    async def announce_entrance(self):
        self.logger.debug("enter")
        await InfoEvent(f"{self.full_name} enters the room.").send(self.websocket, exclude_player=True)
        self.logger.debug("exit")

    async def killed(self):
        self.logger.debug("enter")
        await InfoEvent(f"{self.full_name} has been killed.").send(self.websocket, exclude_player=True)
        self.logger.debug("exit")

    async def respawn(self):
        self.logger.debug("enter")
        await InfoEvent(f"{self.full_name} has respawned.").send(self.websocket, exclude_player=True)
        self.logger.debug("exit")

    async def stop_combat(self):
        self.logger.debug("enter")
        await InfoEvent(f"{self.full_name} has stopped combat.").send(self.websocket, exclude_player=True)
        self.logger.debug("exit")

    async def wander(self):
        self.logger.debug("enter")
        await InfoEvent(f"{self.full_name} wanders off.").send(self.websocket, exclude_player=True)
        self.logger.debug("exit")

    async def get_intelligence_description(self):
        self.logger.debug("enter")
        intelligence = ""
        if self.attributes.intelligence <= 10:
            intelligence = "dimwitted"
        elif 10 <= self.attributes.intelligence < 20:
            intelligence = "slow"
        elif 20 <= self.attributes.intelligence < 30:
            intelligence = "of average intelligence"
        elif 30 <= self.attributes.intelligence < 40:
            intelligence = "smart"
        elif 40 <= self.attributes.intelligence < 50:
            intelligence = "intelligent"
        elif self.attributes.intelligence >= 50:
            intelligence = "genius"
        self.logger.debug("exit")
        return intelligence

    async def get_strength(self):
        pass

    async def get_strength_description(self):
        self.logger.debug("enter")
        physique = ""
        if self.attributes.strength < 10:
            physique = "puny"
        elif 10 <= self.attributes.strength < 20:
            physique = "average"
        elif 20 <= self.attributes.strength < 30:
            physique = "stout"
        elif 30 <= self.attributes.strength < 40:
            physique = "solid"
        elif 40 <= self.attributes.strength < 50:
            physique = "strong"
        elif self.attributes.strength >= 50:
            physique = "godlike"
        self.logger.debug("exit")
        return physique

    async def get_dexterity(self):
        pass

    async def get_dexterity_description(self):
        self.logger.debug("enter")
        dexterity = ""
        if self.attributes.dexterity <= 10:
            dexterity = "sluggish"
        elif 10 < self.attributes.dexterity <= 20:
            dexterity = "slow"
        elif 20 < self.attributes.dexterity <= 30:
            dexterity = "poorly coordinated"
        elif 30 < self.attributes.dexterity <= 40:
            dexterity = "average"
        elif 40 < self.attributes.dexterity <= 50:
            dexterity = "quick"
        elif self.attributes.dexterity > 50:
            dexterity = "lightning fast"
        self.logger.debug("exit")
        return dexterity

    async def get_constitution(self):
        pass

    async def get_constitution_description(self):
        self.logger.debug("enter")
        hitpoint_status = ""
        if self.statuses.current_hp <= 10:
            hitpoint_status = "frail"
        elif 10 <= self.statuses.current_hp < 20:
            hitpoint_status = "weak"
        elif 20 <= self.statuses.current_hp < 30:
            hitpoint_status = "average"
        elif 30 <= self.statuses.current_hp < 40:
            hitpoint_status = "robust"
        elif 40 <= self.statuses.current_hp < 50:
            hitpoint_status = "robust"
        elif self.statuses.current_hp >= 50:
            hitpoint_status = "robust, healthy"
        self.logger.debug("exit")
        return hitpoint_status

    async def get_faith(self):
        pass

    async def get_faith_description(self):
        self.logger.debug("enter")
        faith = ""
        if self.attributes.faith < 10:
            faith = "atheist"
        elif 10 < self.attributes.faith <= 20:
            faith = "spiritual"
        elif 20 < self.attributes.faith <= 30:
            faith = "highly spiritual"
        elif 30 < self.attributes.faith <= 40:
            faith = "devout"
        elif 40 < self.attributes.faith <= 50:
            faith = "holy"
        elif self.attributes.faith > 50:
            faith = "godlike"
        self.logger.debug("exit")
        return faith

    async def get_charisma(self):
        pass

    async def get_charisma_description(self):
        pass

    async def get_experience(self):
        pass

    async def get_level(self):
        pass

    async def get_age(self):
        self.logger.debug("enter")
        age = ""
        if self.age <= 20:
            age = "young"
        elif 20 < self.age <= 50:
            age = "seasoned"
        elif self.age > 50:
            age = "older"
        return age

    # async def get_player_description(self):
    #     self.logger.debug("enter")
    #     age = await self.get_age()
    #     sex = self.pronoun.value.sex
    #     hitpoint_status = await self.get_player_hitpoint_description()
    #     intelligence = await self.get_player_intelligence_description()
    #     physique = await self.get_player_strength_description()
    #     health_status = await self.get_player_health_description()
    #     dexterity = await self.get_player_dexterity_description()
    #     perception = await self.get_player_perception_description(self.pronoun)
    #     determination = await self.get_player_determination_description()
    #     faith = await self.get_player_faith_description()
    #     is_resting = "idly resting" if self.statuses.is_resting else "not resting"

    #     msg = f"""
    #     {self.name} is a level {self.level}, {age} {sex} {self.race.name.capitalize()} {self.player_class.name.capitalize()}. {self.pronoun.value.pronoun.capitalize()} has {self.eye_color} eyes, {self.hair_length}, {self.hair_color} hair and is of {hitpoint_status} health.
    #     {self.pronoun.value.pronoun.capitalize()} has a {physique} body and {self.pronoun.value.pronoun} moves with {dexterity} dexterity.  {self.name} appears {perception}, {intelligence}, {faith}, and {determination}.<br><br>
    #     {self.name} appears to be {health_status} and is {is_resting}. Her mood is {self.statuses.mood.name.lower()}."""
    #     self.logger.debug("exit")
    #     return msg

    async def rest(self, rest: bool):
        self.logger.debug("enter")
        if rest:
            RestEvent("You start resting.", is_resting=True).send(self.websocket)
            self.statuses.is_resting = True
        else:
            if self.statuses.is_resting:
                self.statuses.is_resting = False
                await RestEvent("You are no longer resting.", is_resting=False).send(self.websocket)
            else:
                await InfoEvent("You were not resting to begin with.").send(self.websocket)
        self.logger.debug("exit")

    # cancels all tasks and states you died if you die
    async def die(self, world):
        self.logger.debug("enter")

        # Your done boy.  Done.
        self.in_combat = False

        # state you died
        await InfoEvent("You died.").send(self.websocket)
        await InfoEvent(f"{self.full_name} died.").send(self.websocket, exclude_player=True, scope=SendScopeEnum.ROOM)

        # drop all items
        for item in self.inventory:
            self.room.items.append(item)
        self.inventory = []

        # set player location to death respawn room
        player, world = await world.rooms.move_room(self.DEATH_RESPAWN_ROOM, self, world)

        # alert others in the room that new player has arrived
        await InfoEvent("A bright purple spark floods your vision.").send(self.websocket)
        await InfoEvent(
            f"A bright purple spark floods the room.  When it clears, {self.full_name} is standing naked."
        ).send(self.websocket, exlude_player=True, scope=SendScopeEnum.ROOM)

        # set hits back to max / force health refresh
        self.statuses.current_hp = self.max_hp
        await self.send_status()

        self.logger.debug("exit")
        return player, world

    # shows inventory
    async def get_inventory(self):
        self.logger.debug("enter")
        self.logger.info(f"{self.full_name}: sending updated inventory")
        await InventoryEvent(self.inventory).send(self.websocket)
        self.logger.debug("exit")

    # increases hp when resting
    async def check_rest(self):
        self.logger.debug(f"enter, checking if {self.full_name} is resting..")

        while True:
            # Check resting every 2 seconds
            await asyncio.sleep(WorldSettings.PLAYER_BASE_REST_WAIT_SECS)

            if self.statuses.is_resting:
                self.logger.debug("Checking if resting...")
                if self.statuses.current_hp < self.max_hp:
                    heal = randint(1, 3)
                    if heal == 1:
                        await InfoEvent(f"You recover {heal} hitpoint.").send(self.websocket)
                    else:
                        await InfoEvent(f"You recover {heal} hitpoints.").send(self.websocket)
                    self.statuses.current_hp += 3
                    if self.statuses.current_hp >= self.max_hp:
                        self.statuses.current_hp = self.max_hp
                        await self.set_rest(False)
                        await InfoEvent("You have fully recovered.").send(self.websocket)
                        await InfoEvent(f"{self.full_name} appears to have fully recovered.").send(
                            self.websocket,
                            exclude_player=True,
                            scope=SendScopeEnum.ROOM,
                        )
                    await self.send_status()
