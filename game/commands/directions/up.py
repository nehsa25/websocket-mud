from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import Directions


class Up:
    logger = None
    variations = ["u", "up"]
    opposite = None
    name = "Up"
    type = Directions.UP

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.DOWN
        self.logger.debug("Initializing Up() class")
