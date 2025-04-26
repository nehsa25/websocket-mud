
from core.enums.moods import MoodEnum
from utilities.log_telemetry import LogTelemetryUtility


class StatusesData:
    logger = None
    is_dead = None
    is_resting = None
    is_posioned = None
    is_thirsty = False
    is_hungry = False
    mood = MoodEnum.NORMAL
    posioned = False
    logger = None

    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing status() class")
        self.is_dead = False
        self.is_resting = False
        self.is_posioned = False
        self.is_thirsty = False
        self.is_hungry = False
        self.mood = MoodEnum.NORMAL
