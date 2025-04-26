from typing import Dict, List
from core.data.item_data import ItemData


class ItemFoodData(ItemData):
    effects = List[str]

    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        quality,
        effects: List[str],
    ):
        super().__init__(name, item_type, weight, verb, plural_verb, description, quality)
        self.effects = effects

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
            "effects": [effect.name for effect in self.effects],
        }

    def __repr__(self):
        return f"ItemFoodType(name={self.name}, item_type={self.item_type}, weight={self.weight}, verb={self.verb}, plural_verb={self.plural_verb}, description={self.description}, quality={self.quality}, effects={[effect.name for effect in self.effects]})"
