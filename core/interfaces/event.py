from abc import abstractmethod


class EventInterface:

    # convert to json
    @abstractmethod
    async def to_json(self) -> str:
        pass

    # send message to websocket
    @abstractmethod
    async def send(self, websocket, scope, exclude_player) -> None:
        pass
