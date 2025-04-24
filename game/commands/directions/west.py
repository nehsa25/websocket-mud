from enums.directions import Directions
from utilities.log_telemetry import LogTelemetryUtility


class West:
    logger = None
    variations = ["w", "west", "wes", "we"]
    opposite = None
    name = "West"
    type = Directions.WEST

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.EAST
        self.logger.debug("Initializing West() class")
