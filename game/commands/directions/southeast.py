from enums.directions import Directions
from utilities.log_telemetry import LogTelemetryUtility


class SouthEast:
    logger = None
    variations = ["se", "southeast", "southe"]
    opposite = None
    name = "Southeast"
    type = Directions.SOUTHEAST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.NORTHWEST
        self.logger.debug("Initializing SouthEast() class")
