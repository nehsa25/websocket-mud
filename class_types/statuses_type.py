
from game.enums.moods import Moods
from utilities.log_telemetry import LogTelemetryUtility


class StatusesType:
    logger = None
    is_dead = None
    is_resting = None
    is_posioned = None
    is_thirsty = False
    is_hungry = False
    mood = Moods.NORMAL
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
        self.mood = Moods.NORMAL
