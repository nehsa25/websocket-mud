
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
                "Apple",
                ItemEnum.FOOD.value,
                0.1,
                "crunch",
                "crunches",
                "A crisp, red apple.",
                [EffectsFoodEnum.ALLEVIATE_HUNGER.value],
                100
            ),
            ItemFoodData(
                "Loaf of Bread",
                ItemEnum.FOOD.value,
                0.1,
                "break",
                "breaks",
                "A crusty loaf of bread.",
                effects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
                freshness=100                
            ),
            ItemFoodData(
                "Berries",
                ItemEnum.FOOD.value,
                0.1,
                "squish",
                "squishes",
                "A handful of wild berries.",
                effects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
                freshness=100
            ),
            ItemFoodData(
                "Cooked Meat",
                ItemEnum.FOOD.value,
                0.3,
                "chew",
                "chews",
                "A piece of roasted meat.",
                effects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
                freshness=100
            ),
            ItemFoodData(
                "Cheese Wedge",
                ItemEnum.FOOD.value,
                0.2,
                "smell",
                "smells",
                "A wedge of aged cheese.",
                effects=[EffectsFoodEnum.ALLEVIATE_HUNGER.value],
                freshness=100
            ),
            ItemFoodData(
                "Water Flask",
                ItemEnum.DRINK.value,
                0.5,
                "drink",
                "drinks",
                "A small flask containing drinkable water.",
                effects=[EffectsFoodEnum.ALLEVIATE_THIRST.value, EffectsFoodEnum.POISON1.value],
                freshness=100
            ),
            ItemFoodData(
                "Small Green Bottle",
                ItemEnum.DRINK.value,
                0.5,
                "drink",
                "drinks",
                "A small drink bottle with a greenish liquid inside. It does not smell pleasant.",
                effects=[EffectsFoodEnum.ALLEVIATE_THIRST.value, EffectsFoodEnum.POISON1.value],
                freshness=100
            )
        ]
