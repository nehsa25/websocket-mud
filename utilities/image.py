from core.ai.image import AIImages
from core.game_objects.map import Map
from utilities.log_telemetry import LogTelemetryUtility


class Image:
    logger = None
    map = None
    aiimages = None

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Image() class")
        self.map = Map()
        self.aiimages = AIImages()
