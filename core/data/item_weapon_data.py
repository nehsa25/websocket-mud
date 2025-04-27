from typing import Dict, List

from core.data.item_data import ItemData


class ItemWeaponData(ItemData):
    effects = List[str]
    damage = str  # this is a 1d6 type string
    quality = int

    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        effects: List[str],
        damage,
        quality: int,
    ):
        super().__init__(
            name,
            item_type,
            damage,
            weight,
            verb,
            plural_verb,
            description,         
        )
        self.effects = effects
        self.damage = damage
        self.quality = quality

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert NPC to a dictionary."""
        return {
            "name": self.name,
            "item_type": self.item_type,
            "weight": self.weight,
            "verb": self.verb,
            "plural_verb": self.plural_verb,
            "description": self.description,
            "quality": self.quality,
            "damage": self.damage,
            "effects": [effect.name for effect in self.effects],
        }

    def __repr__(self):
        return f"ItemWeaponType(name={self.name}, item_type={self.item_type}, weight={self.weight}, verb={self.verb}, plural_verb={self.plural_verb}, description={self.description}, quality={self.quality}, attacks={[attack.name for attack in self.attacks]}, damage={self.damage})"