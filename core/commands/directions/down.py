from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import DirectionEnum


class Down:
    logger = None
    variations = ["d", "dow", "down"]
    opposite = None
    name = "Down"
    type = DirectionEnum.DOWN

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.UP
        self.logger.debug("Initializing Down() class")
