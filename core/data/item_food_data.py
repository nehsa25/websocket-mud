from typing import Dict, List
from core.data.item_data import ItemData


class ItemFoodData(ItemData):
    freshness: int

    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        effects: List[str],
        freshness
    ):
        super().__init__(name, item_type, weight, verb, plural_verb, description, effects)
        self.freshness = freshness

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert ItemFoodData to a dictionary."""
        return {
            "name": self.name,
            "item_type": self.item_type,
            "weight": self.weight,
            "verb": self.verb,
            "plural_verb": self.plural_verb,
            "description": self.description,
            "effects": self.effects,
            "freshness": self.freshness
        }
    def __repr__(self):
        return f"ItemFoodData(name={self.name!r}, item_type={self.item_type!r}, weight={self.weight!r}, verb={self.verb!r}, plural_verb={self.plural_verb!r}, description={self.description!r}, effects={self.effects!r}, freshness={self.freshness!r})"