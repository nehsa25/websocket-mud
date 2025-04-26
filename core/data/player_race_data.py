

from typing import Dict, List
from core.enums.race_abilities import RaceAbilityEnum


class PlayerRaceData:
    def __init__(
        self,
        name: str,
        description: str,
        abilities: List[RaceAbilityEnum],
        base_hp: int,
        base_strength: int,
        base_agility: int,
        base_perception: int,
        base_willpower: int,
        base_magic_mana: int,
        base_experience_adjustment: int,
    ):
        self.name = name
        self.description = description
        self.abilities = abilities
        self.base_hp = base_hp
        self.base_strength = base_strength
        self.base_agility = base_agility
        self.base_perception = base_perception
        self.base_willpower = base_willpower
        self.base_magic_mana = base_magic_mana
        self.base_experience_adjustment = base_experience_adjustment

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Race to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "abilities": [ability.value for ability in self.abilities],
            "base_hp": self.base_hp,
            "base_strength": self.base_strength,
            "base_agility": self.base_agility,
            "base_perception": self.base_perception,
            "base_willpower": self.base_willpower,
            "base_magic_mana": self.base_magic_mana,
            "base_experience_adjustment": self.base_experience_adjustment,
        }
