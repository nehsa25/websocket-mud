from enums.directions import Directions
from utilities.log_telemetry import LogTelemetryUtility


class NorthEast:
    logger = None
    variations = ["ne", "northeast", "northe"]
    opposite = None
    name = "Northeast"
    type = Directions.NORTHEAST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.SOUTHWEST
        self.logger.debug("Initializing NorthEast() class")
