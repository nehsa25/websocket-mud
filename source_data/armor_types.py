from core.data.armor_type_data import ArmorTypeData
from core.interfaces.source_data import SourceInterface


class ArmorTypeSource(SourceInterface):
    """
    This class is used to represent the source data for armours for
    initalization of the database.
    """

    def get_data(self):
        return [
            ArmorTypeData(
                name=None,
                description="This item is a type of armor but does not have a specific type.",
            ),
            ArmorTypeData(
                name="Head",
                description="This item protects the head.",
            ),
            ArmorTypeData(
                name="Chest",
                description="This item protects the chest.",
            ),
            ArmorTypeData(
                name="Legs",
                description="This item protects the legs.",
            ),
            ArmorTypeData(
                name="Feet",
                description="This item protects the feet.",
            ),
            ArmorTypeData(
                name="Hands",
                description="This item protects the hands.",
            ),
            ArmorTypeData(
                name="Shield",
                description="This item protects the shield.",
            ),
            ArmorTypeData(
                name="Belt",
                description="This item protects the belt.",
            ),
            ArmorTypeData(
                name="Back",
                description="This item protects the back.",
            ),
        ]
