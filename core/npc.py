from .enums.alignments import AlignmentEnum
from core.interfaces.player import PlayerInterface
from helper.mob import MOBHelper
from core.data.attributes_data import AttributesType
from core.data.statuses_data import StatusesData
from utilities.log_telemetry import LogTelemetryUtility


class Npc(PlayerInterface, MOBHelper):
    eye_color = None
    hair_color = None
    hair_length = None
    tattoes_placement = None
    tattoes_severity = None
    scars = None
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
    statuses = None
    in_combat = None
    ip = None
    inventory = None
    websocket = None
    rest_task = None  # A resting task that check if this user is resting every 2 seconds
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
        alignment=AlignmentEnum.NEUTRAL,
    ):
        self.logger = LogTelemetryUtility.get_logger(
            __name__
        )
        self.logger.debug("Initializing Player() class")
        self.eye_color = eye_color
        self.hair_color = hair_color
        self.hair_length = hair_length
        self.tattoes_placement = tattoes_placement
        self.tattoes_severity = tattoes_severity
        self.scars = scars
        self.name = name
        self.age = age
        self.level = level
        self.current_hp = hp
        self.max_hp = hp
        self.inventory = inventory
        self.location_id = location_id
        self.pronoun = pronoun
        self.race = race
        self.player_class = player_class
        self.ip = ip
        self.websocket = websocket

        # whether player is resting, poisoned, etc.
        self.attributes = AttributesType(
            int=intelligence,
            faith=faith,
            agility=agility,
            perception=perception,
            determination=determination,
            strength=strength,
            logger=self.logger,
        )
        self.statuses = StatusesData()
        self.alignment = alignment

    async def check_combat(self, room):
        pass

    async def break_combat(self, room):
        pass

    async def attack(self, room):
        pass

    async def speak(self, room, world_state):
        pass

    async def move(
        self, direction, world_state, isNpc=True
    ):
        pass

    async def get_hp(self, room):
        pass

    async def get_hp_description(self):
        pass

    async def get_intelligence(self):
        pass

    async def get_intelligence_description(self):
        pass

    async def get_strength(self):
        pass

    async def get_strength_description(self):
        pass

    async def get_dexterity(self):
        pass

    async def get_dexterity_description(self):
        pass

    async def get_constitution(self):
        pass

    async def get_constitution_description(self):
        pass

    async def get_faith(self):
        pass

    async def get_faith_description(self):
        pass

    async def get_charisma(self):
        pass

    async def get_charisma_description(self):
        pass

    async def get_experience(self):
        pass

    async def get_level(self):
        pass

    async def get_age(self):
        pass

    async def get_description(self):
        pass

    async def rest(self, rest: bool):
        pass

    async def die(self, world):
        pass

    # shows inventory
    async def get_inventory(self):
        pass

    # increases hp when resting
    async def check_rest(self):
        pass
