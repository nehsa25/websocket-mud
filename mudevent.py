import json
from race import Races


class MudEvent:
    type = None
    message = None
    races = None


class MudWelcomeEvent:
    type = "hostname_request"
    message = None
    races = Races()
