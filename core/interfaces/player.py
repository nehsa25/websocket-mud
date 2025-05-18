from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from core.data.character_data import CharacterData


class PlayerInterface(ABC):
    name: str
    firstname: str
    lastname: str
    role: str
    email: str
    pin: str
    salt: str
    token: str
    characters: List[
        "CharacterData"
    ]  # the quotes makes this a foward reference (it won't be evaluated until later thus preventing circular imports)
    websocket: object
    websocket_id: str
    selected_character: CharacterData

    @abstractmethod
    async def create_character():
        pass
