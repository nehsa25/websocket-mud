

from game.enums.items import Items
from game.interfaces.source_data import SourceInterface
from class_types.item_light_type import ItemLightType


class LightsourceSource(SourceInterface):
    """
    This class is used to represent the source data for light sources for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemLightType(
                name="Torch",
                item_type=Items.LIGHTSOURCE.value,
                damage=None,
                weight=1,
                verb="flicker",
                plural_verb="flickers",
                description="A wooden torch that provides light.",
                quality=100,
                brightness=30,
            )
        ]
