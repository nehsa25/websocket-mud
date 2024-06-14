import json
from log_utils import LogUtils
from race import Races

class MudEvent:
    type = ""
    message = ""
    races = []
    extra = ""
    
    def __init__(self, type, message, extra):
        self.type = type
        self.message = message
        self.extra = extra


class MudWelcomeEvent:
    type = "hostname_request"
    message = None
    races = Races()
