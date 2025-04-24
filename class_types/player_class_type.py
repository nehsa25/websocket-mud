from typing import Dict, List

from game.enums.class_abilities import ClassAbilities


class PlayerClassType:
    def __init__(
        self,
        name: str,
        description: str,
        abilities: List[ClassAbilities],
        base_experience_adjustment: int,
    ):
        self.name = name
        self.description = description
        self.abilities = abilities
        self.base_experience_adjustment = base_experience_adjustment

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "abilities": [ability.value for ability in self.abilities],
            "base_experience_adjustment": self.base_experience_adjustment,
        }
