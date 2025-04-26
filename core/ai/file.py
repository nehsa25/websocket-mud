import json
from utilities.log_telemetry import LogTelemetryUtility


class AIFile:
    description = None
    file_name = None
    logger = None

    def __init__(self, line) -> None:
        item = json.loads(line)
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.description = item["description"]
        self.file_name = item["file_name"]
