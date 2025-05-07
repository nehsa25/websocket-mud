from core.data.player_data import PlayerData
from core.data.attributes_data import AttributesData
from core.enums.alignments import AlignmentEnum
from core.interfaces.source_data import SourceInterface

from core.enums.races import RaceEnum
from core.enums.player_classes import PlayerClassEnum
from services.auth import AuthService
from utilities.log_telemetry import LogTelemetryUtility
from dontcheckin import Secrets


class PlayerSource(SourceInterface):
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
            PlayerData(
                name="Bink",
                role="admin",
                experience=0,
                level=1,
                money=0,
                pronoun="he",
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
                pin=Secrets.PIN,
                salt=Secrets.SALT,
                token=self.auth_service.generate_token("bink"),
            )
        ]
