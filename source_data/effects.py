from class_types.effects_type import EffectsType
from game.enums.effects import Effects
from game.enums.effects_armor import EffectsArmor
from game.enums.effects_lightsource import EffectsLightsource
from game.enums.effects_weapon import EffectsWeapon
from game.enums.effects_food import EffectsFood
from game.interfaces.source_data import SourceInterface


class EffectSource(SourceInterface):
    """
    This class is used to represent the source data for effects for items (such as poison) for
    initalization of the database.
    """

    def get_data(self):
        return [
            EffectsType(keyword=EffectsFood.CURE_POISON.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsFood.HEALING1.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsFood.HEALING2.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsFood.MANA_POTION.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsFood.POISON1.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsFood.POISON2.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsFood.STAMINA_POTION.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsFood.STRENGTH_POTION.value, type=Effects.FOOD.value),
            EffectsType(keyword=EffectsWeapon.ACID.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.COLD.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.LIGHTNING.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.FIRE.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.HOLY.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.PIERCE.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.SLASH.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.UNHOLY.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.BLUNT.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsWeapon.POISON.value, type=Effects.WEAPON.value),
            EffectsType(keyword=EffectsLightsource.BRIGHTNESS1.value, type=Effects.LIGHTSOURCE.value),
            EffectsType(keyword=EffectsLightsource.BRIGHTNESS2.value, type=Effects.LIGHTSOURCE.value),
            EffectsType(keyword=EffectsLightsource.BRIGHTNESS3.value, type=Effects.LIGHTSOURCE.value),
            EffectsType(keyword=EffectsLightsource.BRIGHTNESS4.value, type=Effects.LIGHTSOURCE.value),
            EffectsType(keyword=EffectsLightsource.BRIGHTNESS5.value, type=Effects.LIGHTSOURCE.value),
            EffectsType(keyword=EffectsLightsource.CAN_SEE_INVISIBLE.value, type=Effects.LIGHTSOURCE.value),
            EffectsType(keyword=EffectsArmor.DEFENCE1.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE2.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE3.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE4.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE5.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE6.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE7.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE8.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE9.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.DEFENCE10.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_ACID.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_COLD.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_LIGHTNING.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_FIRE.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_HOLY.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_UNHOLY.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_POISON.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_SLASH.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_PIERCE.value, type=Effects.ARMOR.value),
            EffectsType(keyword=EffectsArmor.STRONG_BLUNT.value, type=Effects.ARMOR.value),
        ]
