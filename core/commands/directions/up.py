from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import DirectionEnum


class Up:
    logger = None
    variations = ["u", "up"]
    opposite = None
    name = "Up"
    type = DirectionEnum.UP

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = DirectionEnum.DOWN
        self.logger.debug("Initializing Up() class")
