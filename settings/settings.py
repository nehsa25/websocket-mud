import os

from log_utils import Level
from utility import Utility


class MudSettings:
    environment = os.environ.get("MUD_ENV", "development")
    data_location = "C:/src/nehsa/websocket-mud/website/client3/public"
    file_level=Level.DEBUG
    console_level=Level.DEBUG
    image_generation_technology = Utility.AIGeneration.OpenAI
    geminiAImodel = "models/gemini-1.5-pro-latest"
    openAImodel = "sd3" # "sdxl" or "sd3"

    logger = None

    def __init__(self, logger) -> None:
        self.logger = logger
        self.logger.debug("Initializing DevSettings() class")

        if self.environment != "development":
            self.data_location = "/var/www/html/mud-images"
            self.file_level=Level.INFO
            self.console_level=Level.INFO
            