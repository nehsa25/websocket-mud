from typing import Dict
from core.interfaces.attributes import AttributesInterface
from utilities.log_telemetry import LogTelemetryUtility


class AttributesData(AttributesInterface):
    strength: int
    intelligence: int
    wisdom: int
    charisma: int
    constitution: int
    dexterity: int
    luck: int

    def __init__(
        self,
        strength: int = 0,
        intelligence: int = 0,
        wisdom: int = 0,
        charisma: int = 0,
        constitution: int = 0,
        dexterity: int = 0,
        luck: int = 0,
    ) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing AttributesEnum class")
        self.strength = strength
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.constitution = constitution
        self.dexterity = dexterity
        self.luck = luck

    def __str__(self):
        return f"Attributes(strength={self.strength}, intelligence={self.intelligence}, wisdom={self.wisdom}, charisma={self.charisma}, constitution={self.constitution}, dexterity={self.dexterity}, luck={self.luck})"

    def to_dict(self) -> Dict:
        """Helper method to convert Attributes class to a dictionary."""
        return {
            "strength": self.strength,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            "constitution": self.constitution,
            "dexterity": self.dexterity,
            "luck": self.luck,
        }
