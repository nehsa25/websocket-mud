

from typing import Dict, List
from core.enums.race_abilities import RaceAbilityEnum


class PlayerRaceData:
    def __init__(
        self,
        name: str,
        description: str,
        abilities: List[RaceAbilityEnum],
        attributes,
        directives: List[str],
        base_experience_adjustment: int,
    ):
        self.name = name
        self.description = description
        self.abilities = abilities
        self.attributes = attributes
        self.directives = directives
        self.base_experience_adjustment = base_experience_adjustment

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Race to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "abilities": [ability.value for ability in self.abilities],
            "attributes": self.attributes.to_dict(),
            "directives": self.directives if self.directives else None,
            "base_experience_adjustment": self.base_experience_adjustment,
        }