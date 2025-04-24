
from game.enums.effects_food import EffectsFood
from game.enums.items import Items
from game.interfaces.source_data import SourceInterface
from class_types.item_food_type import ItemFoodType


class FoodSource(SourceInterface):
    """
    This class is used to represent the source data for food for
    initalization of the database.
    """

    def get_data(self):
        return [
            ItemFoodType(
                name="Apple",
                item_type=Items.FOOD.value,
                weight=0.1,
                verb="crunch",
                plural_verb="crunches",
                description="A crisp, red apple.",
                quality=None,
                foodeffects=[EffectsFood.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodType(
                "Loaf of Bread",
                Items.FOOD.value,
                None,
                0.1,
                "break",
                "breaks",
                "A crusty loaf of bread.",
                None,
                foodeffects=[EffectsFood.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodType(
                "Berries",
                Items.FOOD.value,
                None,
                0.1,
                "squish",
                "squishes",
                "A handful of wild berries.",
                None,
                foodeffects=[EffectsFood.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodType(
                "Cooked Meat",
                Items.FOOD.value,
                None,
                0.3,
                "chew",
                "chews",
                "A piece of roasted meat.",
                None,
                foodeffects=[EffectsFood.ALLEVIATE_HUNGER.value],
            ),
            ItemFoodType(
                "Cheese Wedge",
                Items.FOOD.value,
                None,
                0.2,
                "smell",
                "smells",
                "A wedge of aged cheese.",
                None,
                foodeffects=[EffectsFood.ALLEVIATE_HUNGER.value],
            ),
                ItemFoodType(
                "Water Flask",
                Items.DRINK.value,
                None,
                0.5,
                "drink",
                "drinks",
                "A small flask containing drinkable water.",
                None,
                foodeffects=[EffectsFood.ALLEVIATE_THIRST.value, EffectsFood.POISON.value],
            ),
            ItemFoodType(
                "Small Green Bottle",
                Items.DRINK.value,
                None,
                0.5,
                "drink",
                "drinks",
                "A small drink bottle with a greenish liquid inside. It does not smell pleasant.",
                None,
                foodeffects=[EffectsFood.ALLEVIATE_THIRST.value, EffectsFood.POISON.value],
            ),
        ]
