from game.enums.defence_effects import DefenceEffects
from game.enums.items import Items
from game.interfaces.source_data import SourceInterface
from class_types.item_armor_type import ItemTypeArmor


class ArmorSource(SourceInterface):
    """
    This class is used to represent the source data for armours for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemTypeArmor(
                name="Kite Shield",
                item_type=Items.ARMOR_SHIELD.value,
                weight=10,
                verb="thunk",
                plural_verb="thunks",
                description="A tall, kite-shaped shield.",
                defences=[
                    DefenceEffects.SHIELD_BONUS1.value
                ],
            )
        ]
