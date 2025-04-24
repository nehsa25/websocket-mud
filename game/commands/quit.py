from game.enums.commands import Commands
from utilities.log_telemetry import LogTelemetryUtility


class Quit:
    logger = None
    command = "quit"
    examples = []
    description = "Quit the game. :("
    type = Commands.QUIT

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Quit() class")

    def execute(self):
        self.logger.debug("Executing Quit command")
        return "Quiting!"
