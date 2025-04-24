from utilities.log_telemetry import LogTelemetryUtility
from enums.directions import Directions


class North:
    logger = None
    variations = ["n", "north", "nor"]
    opposite = None
    name = "North"
    type = Directions.NORTH

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.opposite = Directions.SOUTH
        self.logger.debug("Initializing North() class")
