

from core.data.item_light_data import ItemLightData
from core.enums.items import ItemEnum
from core.interfaces.source_data import SourceInterface


class LightsourceSource(SourceInterface):
    """
    This class is used to represent the source data for light sources for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemLightData(
                name="Torch",
                item_type=ItemEnum.LIGHTSOURCE.value,
                damage=None,
                weight=1,
                verb="flicker",
                plural_verb="flickers",
                description="A wooden torch that provides light.",
                quality=100,
                brightness=30,
            )
        ]
