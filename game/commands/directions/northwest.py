from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import Directions


class NorthWest:
    logger = None
    variations = ["nw", "northwest", "northw"]
    opposite = None
    name = "Northwest"
    type = Directions.NORTHWEST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.SOUTHEAST
        self.logger.debug("Initializing NorthWest() class")
