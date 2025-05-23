from core.data.attributes_data import AttributesData
from core.data.player_class_data import PlayerClassData
from core.enums.monsters import MonsterClassEnum
from core.enums.npc_classes import NpcClassEnum
from core.enums.player_class_abilities import PlayerClassAbilityEnum
from core.enums.player_classes import PlayerClassEnum
from core.interfaces.source_data import SourceInterface


class PlayerClassSource(SourceInterface):
    """
    This class is used to represent the source data for player classes for
    initalization of the database.
    """

    def get_data(self):
        return [
            PlayerClassData(
                PlayerClassEnum.BARBARIAN.value,
                "A fierce warrior relying on brute strength and rage.",
                [PlayerClassAbilityEnum.MARTIAL_PROWESS],
                directives=["savage", "wild"],
                base_experience_adjustment=350,
                playable=True,
                attributes=AttributesData(
                    strength=7,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                PlayerClassEnum.BARD.value,
                "A charismatic musician and storyteller, skilled in both combat and magic.",
                [
                    PlayerClassAbilityEnum.CHARM,
                    PlayerClassAbilityEnum.SUPPORT_MAGIC,
                    PlayerClassAbilityEnum.PLAY_MUSIC,
                    PlayerClassAbilityEnum.PERFORMANCE,
                    PlayerClassAbilityEnum.ILLUSION_MAGIC,
                ],
                directives=["charming", "entertaining"],
                base_experience_adjustment=250,
                playable=True,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=5,
                    luck=2
                ),
            ),
            PlayerClassData(
                PlayerClassEnum.CLERIC.value,
                "A divine caster, channeling the power of their deity.",
                [PlayerClassAbilityEnum.HEALING, PlayerClassAbilityEnum.DIVINE_MAGIC],
                directives=["pious", "devout"],
                base_experience_adjustment=200,
                playable=True,
                attributes=AttributesData(
                    strength=2,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=5,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                PlayerClassEnum.DRUID.value,
                "A nature-attuned caster, commanding the forces of the wild.",
                [PlayerClassAbilityEnum.NATURE_MAGIC, PlayerClassAbilityEnum.SHAPE_SHIFTING],
                directives=["earthy", "wild"],
                base_experience_adjustment=220,
                playable=True,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=2,
                    intelligence=2,
                    wisdom=7,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                PlayerClassEnum.MAGE.value,
                "A scholarly caster, wielding arcane power with precision.",
                [PlayerClassAbilityEnum.MAGIC],
                directives=["intellectual", "studious"],
                base_experience_adjustment=180,
                playable=True,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=7,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                PlayerClassEnum.THIEF.value,
                "A nimble rogue, specializing in larceny and stealth.",
                [PlayerClassAbilityEnum.STEALTH, PlayerClassAbilityEnum.LOCKPICKING],
                directives=["sneaky", "cunning"],
                base_experience_adjustment=340,
                playable=True,
                attributes=AttributesData(
                    strength=0,
                    dexterity=7,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                PlayerClassEnum.WARRIOR.value,
                "A stalwart fighter, skilled in all forms of combat.",
                [PlayerClassAbilityEnum.MARTIAL_PROWESS, PlayerClassAbilityEnum.WEAPON_MASTERY],
                directives=["brave", "strong"],
                base_experience_adjustment=300,
                playable=True,
                attributes=AttributesData(
                    strength=6,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
                PlayerClassData(
                PlayerClassEnum.WARLOCK.value,
                "A stalwart fighter, skilled in all forms of combat and a touch of magic.",
                [PlayerClassAbilityEnum.MARTIAL_PROWESS, PlayerClassAbilityEnum.WEAPON_MASTERY, PlayerClassAbilityEnum.MAGIC],
                directives=["brave", "strong"],
                base_experience_adjustment=500,
                playable=True,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=1,
                    luck=1
                ),
            ),
            PlayerClassData(
                MonsterClassEnum.GHOUL.value,
                "Ghoul",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                MonsterClassEnum.WEREWOLF.value,
                "Werewolf",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                MonsterClassEnum.MUMMY.value,
                "MUMMY",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                MonsterClassEnum.GHOST.value,
                "Ghost",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                MonsterClassEnum.VAMPIRE.value,
                "Vampire",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                MonsterClassEnum.SKELETON.value,
                "Skeleton",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                MonsterClassEnum.ZOMBIE.value,
                "A Zombie",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
            PlayerClassData(
                NpcClassEnum.MERCHANT.value,
                "A merchant",
                [],
                directives=[],
                base_experience_adjustment=300,
                playable=False,
                attributes=AttributesData(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    luck=0
                ),
            ),
        ]
