class GameMessage:

    def __init__(self, type: str, payload: str, origin: str, websocket: object):
        self.type = type
        self.payload = payload
        self.origin = origin
        self.websocket = websocket
