from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import Directions


class SouthWest:
    logger = None
    variations = ["sw", "southwest", "southw"]
    opposite = None
    name = "Southwest"
    type = Directions.SOUTHWEST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.NORTHEAST
        self.logger.debug("Initializing SouthWest() class")
