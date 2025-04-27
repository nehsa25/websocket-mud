from typing import List


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
