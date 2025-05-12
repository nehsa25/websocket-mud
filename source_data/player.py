from core.data.player_data import PlayerData
from core.enums.roles import RoleEnum
from core.interfaces.source_data import SourceInterface

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
                firstname="Jesse",
                lastname="Stone",
                role=RoleEnum.ADMIN.value,
                email="jesse.stone@nehsa.net",
                pin=Secrets.PIN,
                salt=Secrets.SALT
            )
        ]
