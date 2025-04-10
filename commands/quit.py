from log_utils import LogUtils
from utility import Utility

class Quit(Utility):
    logger = None
    command = "quit"
    examples = []
    description = "Quit the game. :("
    type = Utility.Commands.QUIT
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Quit() class", self.logger)

    def execute(self):
        LogUtils.debug("Executing Quit command", self.logger)
        return "Quiting!"