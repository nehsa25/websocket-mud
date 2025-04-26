from core.data.player_class_data import PlayerClassData
from core.enums.player_class_abilities import PlayerClassAbilityEnum
from core.interfaces.source_data import SourceInterface


class PlayerClassSource(SourceInterface):
    """
    This class is used to represent the source data for player classes for
    initalization of the database.
    """

    def get_data(self):
        return [
            PlayerClassData(
                "Barbarian",
                "A fierce warrior relying on brute strength and rage.",
                [PlayerClassAbilityEnum.MARTIAL_PROWESS],
                base_experience_adjustment=350,
            ),
            PlayerClassData(
                "Bard",
                "A charismatic musician and storyteller, skilled in both combat and magic.",
                [
                    PlayerClassAbilityEnum.CHARM,
                    PlayerClassAbilityEnum.SUPPORT_MAGIC,
                    PlayerClassAbilityEnum.PLAY_MUSIC,
                    PlayerClassAbilityEnum.PERFORMANCE,
                    PlayerClassAbilityEnum.ILLUSION_MAGIC,
                ],
                base_experience_adjustment=250,
            ),
            PlayerClassData(
                "Berserker",
                "An uncontrollable warrior filled with rage and bloodlust.",
                [PlayerClassAbilityEnum.FRENZY, PlayerClassAbilityEnum.MARTIAL_PROWESS],
                base_experience_adjustment=400,
            ),
            PlayerClassData(
                "Cleric",
                "A divine caster, channeling the power of their deity.",
                [PlayerClassAbilityEnum.HEALING, PlayerClassAbilityEnum.DIVINE_MAGIC],
                base_experience_adjustment=200,
            ),
            PlayerClassData(
                "Druid",
                "A nature-attuned caster, commanding the forces of the wild.",
                [PlayerClassAbilityEnum.NATURE_MAGIC, PlayerClassAbilityEnum.SHAPE_SHIFTING],
                base_experience_adjustment=220,
            ),
            PlayerClassData(
                "Knight",
                "A heavily armored warrior, sworn to protect the realm.",
                [PlayerClassAbilityEnum.DEFENSE, PlayerClassAbilityEnum.MARTIAL_PROWESS],
                base_experience_adjustment=320,
            ),
            PlayerClassData(
                "Mage",
                "A scholarly caster, wielding arcane power with precision.",
                [PlayerClassAbilityEnum.MAGIC],
                base_experience_adjustment=180,
            ),
            PlayerClassData(
                "Ranger",
                "A skilled tracker and survivalist, at home in the wilderness.",
                [PlayerClassAbilityEnum.TRACKING, PlayerClassAbilityEnum.SURVIVAL],
                base_experience_adjustment=310,
            ),
            PlayerClassData(
                "Rogue",
                "A stealthy trickster, skilled in deception and subterfuge.",
                [PlayerClassAbilityEnum.STEALTH, PlayerClassAbilityEnum.TRICKERY],
                base_experience_adjustment=330,
            ),
            PlayerClassData(
                "Thief",
                "A nimble rogue, specializing in larceny and stealth.",
                [PlayerClassAbilityEnum.STEALTH, PlayerClassAbilityEnum.LOCKPICKING],
                base_experience_adjustment=340,
            ),
            PlayerClassData(
                "Warrior",
                "A stalwart fighter, skilled in all forms of combat.",
                [PlayerClassAbilityEnum.MARTIAL_PROWESS, PlayerClassAbilityEnum.WEAPON_MASTERY],
                base_experience_adjustment=300,
            ),
        ]
