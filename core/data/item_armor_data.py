from typing import Dict, List


from core.data.item_data import ItemData


class ItemArmorData(ItemData):
    effects = List[str]

    def __init__(self, name, item_type, weight, verb, plural_verb, description, quality, armor_type, effects):
        super().__init__(name, item_type, weight, verb, plural_verb, description, quality)
        self.armor_type = armor_type
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
            "armor_type": self.armor_type,
            "effects": [effect.name for effect in self.effects]
        }

    def __repr__(self):
        return f"ItemTypeArmor(name={self.name}, item_type={self.item_type}, weight={self.weight}, verb={self.verb}, plural_verb={self.plural_verb}, description={self.description}, quality={self.quality}, defences={[defence.name for defence in self.defences]})"
