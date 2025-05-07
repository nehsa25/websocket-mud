from core.data.attributes_data import AttributesData
from core.data.player_race_data import PlayerRaceData
from core.enums.race_abilities import RaceAbilityEnum
from core.enums.races import RaceEnum
from core.interfaces.source_data import SourceInterface


class PlayerRaceSource(SourceInterface):
    """
    This class is used to represent the source data for player races for
    initalization of the database.
    """

    def get_data(self):
        return [
            PlayerRaceData(
                RaceEnum.ARGUNA.value,
                "A towering, lumbering race native to the Crosse Mountains. Arguna are renowned for their immense strength and resilience, though their size often makes them slower and less agile. They are stoic and determined, enduring hardships that would break lesser beings.",
                [
                    RaceAbilityEnum.HEIGHTENED_STRENGTH,
                    RaceAbilityEnum.POISON_RESISTANCE,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=["answers slowly", "speaks in a deep, rumbling voice"],
                base_experience_adjustment=400,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.EAREA.value,
                "Enigmatic telepathic beings from the Alair Plains. Earea are believed to be a hive-minded race, their origins shrouded in mystery. They possess potent mental abilities, allowing for communication and manipulation of thoughts, but are physically frail.",
                [
                    RaceAbilityEnum.TELEPATHIC,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=300,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.FAE.value,
                "Graceful and ethereal beings from the enchanted Twilight Glades. Fae are deeply connected to the magical energies of the world, possessing an innate affinity for magic. They are often associated with nature and possess keen senses, though they can be physically delicate.",
                [
                    RaceAbilityEnum.DARKVISION,
                    RaceAbilityEnum.MAGIC,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=250,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.GOBLIN.value,
                "Small, green-skinned humanoids known for their cunning and scavenging skills. Goblins thrive in dark, cramped environments and are often seen as pests or nuisances. Though physically weak, they possess a knack for traps and trickery.",
                [
                    RaceAbilityEnum.DARKVISION,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=200,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.HALFLING.value,
                "Cheerful and stout folk from the rolling Greenmeadows. Halflings are renowned for their love of comfort, good food, and peaceful living. They are surprisingly agile and possess an uncanny knack for avoiding danger, often attributed to their inherent luck and sharp intuition.",
                [
                    RaceAbilityEnum.HEIGHTENED_INTUITION,
                    RaceAbilityEnum.HEIGHTENED_AGILITY,
                    RaceAbilityEnum.LUCK,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=150,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.HALFOGRE.value,
                "The result of unions between humans and ogres, Half-Ogres inherit the brute strength of their ogre parentage. They are often ostracized by both societies, leading to a tough and resilient nature. While not as intelligent as humans, they possess a formidable willpower.",
                [
                    RaceAbilityEnum.HEIGHTENED_STRENGTH2,
                    RaceAbilityEnum.HEIGHTENED_WILL,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=450,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.KOBOLD.value,
                "Small, reptilian humanoids often dwelling in warrens or underground complexes. Kobolds are known for their cunning and agility, often relying on traps and ambushes to overcome their physical limitations. They have a strong sense of community and are fiercely loyal to their tribe.",
                [
                    RaceAbilityEnum.HEIGHTENED_INTUITION,
                    RaceAbilityEnum.HEIGHTENED_AGILITY,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=175,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.NYRRISS.value,
                "A race adapted to the treacherous swamps of Nyrriss. Nyriss are known for their resilience to poisons and diseases, as well as their highly developed senses of taste and smell. They are often reclusive and distrustful of outsiders.",
                [
                    RaceAbilityEnum.POISON_IMMUNITY,
                    RaceAbilityEnum.HEIGHTENED_TASTE,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=225,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.ORC.value,
                "Large, muscular humanoids with a reputation for ferocity and warfare. Orcs are known for their incredible strength and toughness, often favoring brute force over finesse. They possess a keen sense of smell and a strong tribal culture.",
                [
                    RaceAbilityEnum.HEIGHTENED_STRENGTH,
                    RaceAbilityEnum.HEIGHTENED_WILL,
                    RaceAbilityEnum.HEIGHTENED_SMELL,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=350,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.HUMAN.value,
                "Adaptable and versatile inhabitants of Illisurom. Humans are known for their capacity for learning and specialization, excelling in a wide range of fields. They lack the inherent strengths of other races but possess a drive and ambition that allows them to overcome their limitations.",
                [
                    RaceAbilityEnum.SPECIALIZATION,
                ],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=0,
                playable=True,
            ),
            PlayerRaceData(
                RaceEnum.WEREWOLF.value,
                "Werewolves.",
                [],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=0,
                playable=False,
            ),
            PlayerRaceData(
                RaceEnum.UNDEAD.value,
                "Undead.",
                [],
                attributes=AttributesData(
                    strength=10,
                    dexterity=10,
                    constitution=10,
                    intelligence=10,
                    wisdom=10,
                    charisma=10,
                ),
                directives=[],
                base_experience_adjustment=0,
                playable=False,
            ),
        ]
