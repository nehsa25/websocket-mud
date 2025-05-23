

from core.data.item_lightsource_data import ItemLightsourceData
from core.enums.items import ItemEnum
from core.interfaces.source_data import SourceInterface


class LightsourceSource(SourceInterface):
    """
    This class is used to represent the source data for light sources for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemLightsourceData(
                name="Torch",
                item_type=ItemEnum.LIGHTSOURCE.value,
                weight=1,
                verb="flicker",
                plural_verb="flickers",
                description="A wooden torch that provides light.",
                effects=[],
                brightness=30,
            )
        ]
