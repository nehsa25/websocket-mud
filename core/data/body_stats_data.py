from utilities.log_telemetry import LogTelemetryUtility


class BodyStatsData:
    hp = 50
    strength = 3  # 0 - 30
    agility = 3  # 0 - 30
    location = 0
    perception = 50

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Stats() class")
