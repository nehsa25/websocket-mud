from core.data.item_armor_data import ItemArmorData
from core.enums.armor_types import ArmorTypeEnum
from core.enums.items import ItemEnum
from core.interfaces.source_data import SourceInterface


class ArmorSource(SourceInterface):
    """
    This class is used to represent the source data for armours for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemArmorData(
                name="Kite Shield",
                item_type=ItemEnum.ARMOR.value,
                weight=10,
                verb="thunk",
                plural_verb="thunks",
                description="A tall, kite-shaped shield.",
                quality=100,
                armor_type=ArmorTypeEnum.SHIELD.value,
                effects=[],
            )
        ]
