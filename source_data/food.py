
from core.data.item_food_data import ItemFoodData
from core.enums.effects_foods import EffectsFoodEnum
from core.enums.items import ItemEnum
from core.interfaces.source_data import SourceInterface


class FoodSource(SourceInterface):
    """
    This class is used to represent the source data for food for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemFoodData(
                name="Apple",
                item_type=ItemEnum.FOOD.value,
                weight=0.1,
                verb="crunch",
                plural_verb="crunches",
                description="A crisp, red apple.",
                quality=None,
                foodeffects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodData(
                "Loaf of Bread",
                ItemEnum.FOOD.value,
                None,
                0.1,
                "break",
                "breaks",
                "A crusty loaf of bread.",
                None,
                foodeffects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodData(
                "Berries",
                ItemEnum.FOOD.value,
                None,
                0.1,
                "squish",
                "squishes",
                "A handful of wild berries.",
                None,
                foodeffects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodData(
                "Cooked Meat",
                ItemEnum.FOOD.value,
                None,
                0.3,
                "chew",
                "chews",
                "A piece of roasted meat.",
                None,
                foodeffects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodData(
                "Cheese Wedge",
                ItemEnum.FOOD.value,
                None,
                0.2,
                "smell",
                "smells",
                "A wedge of aged cheese.",
                None,
                foodeffects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
            ),
                ItemFoodData(
                "Water Flask",
                ItemEnum.DRINK.value,
                None,
                0.5,
                "drink",
                "drinks",
                "A small flask containing drinkable water.",
                None,
                foodeffects=[EffectsFoodEnum.ALLEVIATE_THIRST.value, EffectsFoodEnum.POISON.value],
            ),
            ItemFoodData(
                "Small Green Bottle",
                ItemEnum.DRINK.value,
                None,
                0.5,
                "drink",
                "drinks",
                "A small drink bottle with a greenish liquid inside. It does not smell pleasant.",
                None,
                foodeffects=[EffectsFoodEnum.ALLEVIATE_THIRST.value, EffectsFoodEnum.POISON.value],
            ),
        ]
