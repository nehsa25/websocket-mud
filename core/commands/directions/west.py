from enums.directions import DirectionEnum
from utilities.log_telemetry import LogTelemetryUtility


class West:
    logger = None
    variations = ["w", "west", "wes", "we"]
    opposite = None
    name = "West"
    type = DirectionEnum.WEST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.EAST
        self.logger.debug("Initializing West() class")
