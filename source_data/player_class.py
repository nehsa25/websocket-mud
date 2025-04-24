from game.enums.class_abilities import ClassAbilities
from game.interfaces.source_data import SourceInterface
from class_types.player_class_type import PlayerClassType


class PlayerClassSource(SourceInterface):
    """
    This class is used to represent the source data for player classes for
    initalization of the database.
    """

    def get_data(self):
        return [
            PlayerClassType(
                "Barbarian",
                "A fierce warrior relying on brute strength and rage.",
                [ClassAbilities.MARTIAL_PROWESS],
                base_experience_adjustment=350,
            ),
            PlayerClassType(
                "Bard",
                "A charismatic musician and storyteller, skilled in both combat and magic.",
                [
                    ClassAbilities.CHARM,
                    ClassAbilities.SUPPORT_MAGIC,
                    ClassAbilities.PLAY_MUSIC,
                    ClassAbilities.PERFORMANCE,
                    ClassAbilities.ILLUSION_MAGIC,
                ],
                base_experience_adjustment=250,
            ),
            PlayerClassType(
                "Berserker",
                "An uncontrollable warrior filled with rage and bloodlust.",
                [ClassAbilities.FRENZY, ClassAbilities.MARTIAL_PROWESS],
                base_experience_adjustment=400,
            ),
            PlayerClassType(
                "Cleric",
                "A divine caster, channeling the power of their deity.",
                [ClassAbilities.HEALING, ClassAbilities.DIVINE_MAGIC],
                base_experience_adjustment=200,
            ),
            PlayerClassType(
                "Druid",
                "A nature-attuned caster, commanding the forces of the wild.",
                [ClassAbilities.NATURE_MAGIC, ClassAbilities.SHAPE_SHIFTING],
                base_experience_adjustment=220,
            ),
            PlayerClassType(
                "Knight",
                "A heavily armored warrior, sworn to protect the realm.",
                [ClassAbilities.DEFENSE, ClassAbilities.MARTIAL_PROWESS],
                base_experience_adjustment=320,
            ),
            PlayerClassType(
                "Mage",
                "A scholarly caster, wielding arcane power with precision.",
                [ClassAbilities.MAGIC],
                base_experience_adjustment=180,
            ),
            PlayerClassType(
                "Ranger",
                "A skilled tracker and survivalist, at home in the wilderness.",
                [ClassAbilities.TRACKING, ClassAbilities.SURVIVAL],
                base_experience_adjustment=310,
            ),
            PlayerClassType(
                "Rogue",
                "A stealthy trickster, skilled in deception and subterfuge.",
                [ClassAbilities.STEALTH, ClassAbilities.TRICKERY],
                base_experience_adjustment=330,
            ),
            PlayerClassType(
                "Thief",
                "A nimble rogue, specializing in larceny and stealth.",
                [ClassAbilities.STEALTH, ClassAbilities.LOCKPICKING],
                base_experience_adjustment=340,
            ),
            PlayerClassType(
                "Warrior",
                "A stalwart fighter, skilled in all forms of combat.",
                [ClassAbilities.MARTIAL_PROWESS, ClassAbilities.WEAPON_MASTERY],
                base_experience_adjustment=300,
            ),
        ]
