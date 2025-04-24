from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import Directions


class Down:
    logger = None
    variations = ["d", "dow", "down"]
    opposite = None
    name = "Down"
    type = Directions.DOWN

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.UP
        self.logger.debug("Initializing Down() class")
