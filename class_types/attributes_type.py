from utilities.log_telemetry import LogTelemetryUtility


class AttributesType:
    logger = None
    intelligence = 0
    faith = 0
    max_hp = 0
    strength = 0
    agility = 0
    perception = 0
    determination = 0

    def __init__(
        self, int, faith, agility, perception, determination, strength
    ) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing status() class")
        self.strength = strength
        self.determination = determination
        self.perception = perception
        self.agility = agility
        self.faith = faith
        self.intelligence = int
