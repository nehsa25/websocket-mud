from abc import ABC, abstractmethod


class WebsocketInterface(ABC):
    """ This is for communication with the websocket server"""
    
    type: str
    message: str
    websocket: object

    # convert to json
    @abstractmethod
    async def to_json(self) -> str:
        pass

    # send message to websocket
    @abstractmethod
    async def send(self, websocket, scope, exclude_player) -> None:
        pass
