from typing import Dict, List

from core.enums.player_class_abilities import PlayerClassAbilityEnum


class PlayerClassData:
    def __init__(
        self,
        name: str,
        description: str,
        abilities: List[PlayerClassAbilityEnum],
        directives: List[str],
        base_experience_adjustment: int,
        playable: bool = True,
    ):
        self.name = name
        self.description = description
        self.abilities = abilities
        self.directives = directives
        self.base_experience_adjustment = base_experience_adjustment
        self.playable = playable

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "abilities": [ability.value for ability in self.abilities],
            "directives": [directive for directive in self.directives],
            "base_experience_adjustment": self.base_experience_adjustment,
            "playable": self.playable,
        }
