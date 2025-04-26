from core.data.effects_data import EffectsData
from core.enums.effects import EffectEnum
from core.enums.effects_armor import EffectsArmorEnum
from core.enums.effects_lightsources import EffectsLightsourceEnum
from core.enums.effects_weapons import EffectsWeaponEnum
from core.enums.effects_foods import EffectsFoodEnum
from core.interfaces.source_data import SourceInterface


class EffectSource(SourceInterface):
    """
    This class is used to represent the source data for effects for items (such as poison) for
    initalization of the database.
    """

    def get_data(self):
        return [
            EffectsData(keyword=EffectsFoodEnum.CURE_POISON.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsFoodEnum.HEALING1.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsFoodEnum.HEALING2.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsFoodEnum.MANA_POTION.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsFoodEnum.POISON1.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsFoodEnum.POISON2.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsFoodEnum.STAMINA_POTION.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsFoodEnum.STRENGTH_POTION.value, type=EffectEnum.FOOD.value),
            EffectsData(keyword=EffectsWeaponEnum.ACID.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.COLD.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.LIGHTNING.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.FIRE.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.HOLY.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.PIERCE.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.SLASH.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.UNHOLY.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.BLUNT.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsWeaponEnum.POISON.value, type=EffectEnum.WEAPON.value),
            EffectsData(keyword=EffectsLightsourceEnum.BRIGHTNESS1.value, type=EffectEnum.LIGHTSOURCE.value),
            EffectsData(keyword=EffectsLightsourceEnum.BRIGHTNESS2.value, type=EffectEnum.LIGHTSOURCE.value),
            EffectsData(keyword=EffectsLightsourceEnum.BRIGHTNESS3.value, type=EffectEnum.LIGHTSOURCE.value),
            EffectsData(keyword=EffectsLightsourceEnum.BRIGHTNESS4.value, type=EffectEnum.LIGHTSOURCE.value),
            EffectsData(keyword=EffectsLightsourceEnum.BRIGHTNESS5.value, type=EffectEnum.LIGHTSOURCE.value),
            EffectsData(keyword=EffectsLightsourceEnum.CAN_SEE_INVISIBLE.value, type=EffectEnum.LIGHTSOURCE.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE1.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE2.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE3.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE4.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE5.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE6.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE7.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE8.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE9.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.DEFENCE10.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_ACID.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_COLD.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_LIGHTNING.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_FIRE.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_HOLY.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_UNHOLY.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_POISON.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_SLASH.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_PIERCE.value, type=EffectEnum.ARMOR.value),
            EffectsData(keyword=EffectsArmorEnum.STRONG_BLUNT.value, type=EffectEnum.ARMOR.value),
        ]
