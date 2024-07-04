import inspect
from log_utils import LogUtils
from utility import Utility

class NpcMob(Utility):
    name = ""
    title=""
    description=""
    common_phrases = []
    interests = []
    schedules = []

    def __init__(self, logger, name="", description="", title=""):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Npc() class", logger)
        if name == "":
            self.name = self.generate_name(include_identifier=False)
        else:
            self.name = name
            
        self.title = title
        self.description = description
        
    def generate(self):
        LogUtils.info(f"Generating Npc {self.name}...", self.logger)
        return self

        