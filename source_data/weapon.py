from game.enums.items import Items
from game.interfaces.source_data import SourceInterface
from class_types.item_weapon_type import ItemWeaponType


class WeaponSource(SourceInterface):
    """
    This class is used to represent the source data for weapons for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemWeaponType(
                name="Falchion",
                item_type=Items.WEAPON.value,
                damage="1d6",
                weight=4,
                verb="swing",
                plural_verb="swings",
                description="A curved sword with a single edge.",
                quality=100,
                attacks=[],
            )
        ]
