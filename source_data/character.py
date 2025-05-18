from core.data.attributes_data import AttributesData
from core.data.character_data import CharacterData
from core.enums.alignments import AlignmentEnum
from core.enums.body_types import BodyTypesEnum
from core.enums.eye_brows import EyeBrowEnum
from core.enums.eye_colors import EyeColorEnum
from core.enums.facial_hair import FacialHairEnum
from core.enums.hair_colors import HairColorEnum
from core.enums.hair_styles import HairStylesEnum
from core.enums.sex import SexEnum
from core.interfaces.source_data import SourceInterface

from core.enums.races import RaceEnum
from core.enums.player_classes import PlayerClassEnum
from services.auth import AuthService
from utilities.log_telemetry import LogTelemetryUtility


class CharacterSource(SourceInterface):
    """
    This class is used to represent the source data for player for
    initalization of the database.
    """

    auth_service = None

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing PlayerSource")
        self.auth_service = AuthService()

    def get_data(self):
        return [
            CharacterData(
                firstname="Bink",
                lastname="Brightlights",
                experience=0,
                level=1,
                money=0,
                sex=SexEnum.MALE.value,
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                alignment=AlignmentEnum.NEUTRAL.value,
                player_race=RaceEnum.HUMAN.value,
                player_class=PlayerClassEnum.WARRIOR.value,
                room_id=1,
                eye_brow=EyeBrowEnum.THIN.value,
                eye_color=EyeColorEnum.HAZEL.value,
                body_type=BodyTypesEnum.AVERAGE.value,
                facial_hair=FacialHairEnum.BEARD.value,
                hair_color=HairColorEnum.BROWN.value,
                hair_style=HairStylesEnum.BALD.value,
            ),
            CharacterData(
                firstname="Ashen",
                lastname="Nehsa",
                experience=0,
                level=1,
                money=0,
                sex=SexEnum.MALE.value,
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                alignment=AlignmentEnum.NEUTRAL.value,
                player_race=RaceEnum.HUMAN.value,
                player_class=PlayerClassEnum.WARRIOR.value,
                room_id=1,
                eye_brow=EyeBrowEnum.ARCHED.value,
                eye_color=EyeColorEnum.HAZEL.value,
                body_type=BodyTypesEnum.THIN.value,
                facial_hair=FacialHairEnum.BEARD.value,
                hair_color=HairColorEnum.BROWN.value,
                hair_style=HairStylesEnum.BALD.value,
            ),
        ]
