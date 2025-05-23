from typing import Dict
from utilities.log_telemetry import LogTelemetryUtility


class MobTypeData:
    type = ""  # MobTypeEnum
    description = ""

    def __init__(self, type: str, description: str = ""):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.type = type
        self.description = description
        self.logger.debug(f"Stats initialized with type: {self.type} and description: {self.description}")

    def __repr__(self):
        return f"MobTypeData(type={self.type}, description={self.description})"
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "description": self.description,
        }