from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import DirectionEnum


class South:
    logger = None
    variations = ["s", "south", "sou"]
    opposite = None
    name = "South"
    type = DirectionEnum.SOUTH

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.NORTH
        self.logger.debug("Initializing South() class")
