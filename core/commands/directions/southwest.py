from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import DirectionEnum


class SouthWest:
    logger = None
    variations = ["sw", "southwest", "southw"]
    opposite = None
    name = "Southwest"
    type = DirectionEnum.SOUTHWEST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.NORTHEAST
        self.logger.debug("Initializing SouthWest() class")
