from typing import Dict, List

from core.data.item_data import ItemData


class ItemWeaponData(ItemData):
    damage = str  # this is a 1d6 type string
    quality = int
    speed = int

    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        effects: List[str],
        quality: int,
        damage: str,
        speed: int,
    ):
        super().__init__(name, item_type, weight, verb, plural_verb, description, effects)
        self.quality = quality
        self.damage = damage
        self.speed = speed

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert ItemWeaponData to a dictionary."""
        return {
            "name": self.name,
            "item_type": self.item_type,
            "weight": self.weight,
            "verb": self.verb,
            "plural_verb": self.plural_verb,
            "description": self.description,
            "effects": [effect.name for effect in self.effects],
            "quality": self.quality,
            "damage": self.damage,
            "speed": self.speed,
        }

    def __repr__(self):
        return f"ItemWeaponData(name={self.name!r}, item_type={self.item_type!r}, weight={self.weight!r}, verb={self.verb!r}, plural_verb={self.plural_verb!r}, description={self.description!r}, effects={self.effects!r}, quality={self.quality!r}, damage={self.damage!r}, speed={self.speed!r})"
