import os

from enums.ai_generation_services import AIGeneration
from enums.level import Level


class GlobalSettings:
    ENVIRONMENT = os.environ.get("MUD_ENV", "development")
    DATABASE_PATH = os.path.join(os.getcwd(), "game_data.db")
    DATABASE_STRING = "sqlite+aiosqlite:///game_data.db"
    DATA_LOCATION = "C:/src/nehsa/websocket-mud/website/client3/public"
    FILE_LEVEL = Level.DEBUG
    CONSOLE_LEVEL = Level.DEBUG
    IMAGE_GENERATION_TECHNOLOGY = AIGeneration.OpenAI
    GEMINI_AI_MODEL = "models/gemini-1.5-pro-latest"
    OPENAI_MODEL = "sd3"  # "sdxl" or "sd3"
    LOG_LOCATION = None

    logger = None

    def __init__(self) -> None:
        self.LOG_LOCATION = os.path.join(os.getcwd(), "logs")

        if self.ENVIRONMENT != "development":
            self.DATA_LOCATION = "/var/www/html/mud-images"
            self.FILE_LEVEL = Level.INFO
            self.CONSOLE_LEVEL = Level.INFO