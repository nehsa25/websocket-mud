from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import DirectionEnum


class East:
    logger = None
    variations = ["e", "east", "eas", "ea"]
    opposite = None
    name = "East"
    type = DirectionEnum.EAST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.WEST
        self.logger.debug("Initializing East() class")
