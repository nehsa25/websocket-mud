from core.data.item_weapon_data import ItemWeaponData
from core.enums.items import ItemEnum
from core.interfaces.source_data import SourceInterface


class WeaponSource(SourceInterface):
    """
    This class is used to represent the source data for weapons for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemWeaponData(
                name="Falchion",
                item_type=ItemEnum.WEAPON.value,
                weight=4,
                verb="swing",
                plural_verb="swings",
                description="A curved sword with a single edge.",
                effects=[],
                quality=100,
                damage="1d6", 
                speed=100
            )
        ]
