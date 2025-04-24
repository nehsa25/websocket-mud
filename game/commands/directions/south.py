from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import Directions


class South:
    logger = None
    variations = ["s", "south", "sou"]
    opposite = None
    name = "South"
    type = Directions.SOUTH

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.NORTH
        self.logger.debug("Initializing South() class")
