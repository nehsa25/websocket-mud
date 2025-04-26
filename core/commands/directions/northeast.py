from enums.directions import DirectionEnum
from utilities.log_telemetry import LogTelemetryUtility


class NorthEast:
    logger = None
    variations = ["ne", "northeast", "northe"]
    opposite = None
    name = "Northeast"
    type = DirectionEnum.NORTHEAST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.SOUTHWEST
        self.logger.debug("Initializing NorthEast() class")
