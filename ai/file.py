import json
from utility import Utility


class AIFile(Utility):
    description = None
    file_name = None
    logger = None

    def __init__(self, line, logger) -> None:
        item = json.loads(line)
        self.logger = logger
        self.description = item["description"]
        self.file_name = item["file_name"]