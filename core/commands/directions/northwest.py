from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import DirectionEnum


class NorthWest:
    logger = None
    variations = ["nw", "northwest", "northw"]
    opposite = None
    name = "Northwest"
    type = DirectionEnum.NORTHWEST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.SOUTHEAST
        self.logger.debug("Initializing NorthWest() class")
