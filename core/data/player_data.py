from __future__ import annotations
from typing import Dict, List

from core.data.character_data import CharacterData
from core.enums.roles import RoleEnum
from core.interfaces.player import PlayerInterface
from utilities.log_telemetry import LogTelemetryUtility


class PlayerData(PlayerInterface):
    logger = None
    websocket_id: str
    token: str = ""

    def __init__(self, firstname="", lastname="", role=RoleEnum.USER.value, email="", pin="", salt="", websocket=None):
        logger = LogTelemetryUtility.get_logger(__name__)
        logger.debug("Initializing PlayerData")
        self.websocket = websocket
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.email = email
        self.pin = pin
        self.salt = salt
        self.characters: List[CharacterData] = []
        self.selected_character = None

    @property
    def name(self) -> str:
        return f"{self.firstname} {self.lastname}"

    def __str__(self):
        return f"Player(firstname={self.firstname}, lastname={self.lastname}, email={self.email})"

    def to_dict(self) -> Dict:
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "role": self.role,
            "email": self.email,
            "pin": self.pin,
            "salt": self.salt,
            "characters": [character.to_dict() for character in self.characters],
        }

    async def create_character(self, firstname: str, lastname: str, room):
        character = CharacterData(firstname=firstname, lastname=lastname, room=room)
        self.characters.append(character)
