from typing import Dict, List


class ItemData:
    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        effects: List[str] = None,
    ):
        self.name = name
        self.item_type = item_type
        self.weight = weight
        self.verb = verb
        self.plural_verb = plural_verb
        self.description = description
        self.effects = effects if effects is not None else []

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "name": self.name,
            "item_type": self.item_type,
            "weight": self.weight,
            "verb": self.verb,
            "plural_verb": self.plural_verb,
            "description": self.description,
            "effects": [effect for effect in self.effects],
        }
    