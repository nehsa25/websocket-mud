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
                damage="1d6",
                weight=4,
                verb="swing",
                plural_verb="swings",
                description="A curved sword with a single edge.",
                quality=100,
                attacks=[],
            )
        ]
