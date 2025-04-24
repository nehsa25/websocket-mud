

from game.enums.race_abilities import RaceAbilities
from game.interfaces.source_data import SourceInterface
from class_types.player_race_type import PlayerRaceType


class PlayerRaceSource(SourceInterface):
    """
    This class is used to represent the source data for player races for
    initalization of the database.
    """

    def get_data(self):
        return [
            PlayerRaceType(
                "Arguna",
                "A towering, lumbering race native to the Ironpeak Mountains. Arguna are renowned for their immense strength and resilience, though their size often makes them slower and less agile. They are stoic and determined, enduring hardships that would break lesser beings.",
                [
                    RaceAbilities.HEIGHTENED_STRENGTH,
                    RaceAbilities.POISON_RESISTANCE,
                ],
                base_hp=120,
                base_strength=18,
                base_agility=8,
                base_perception=10,
                base_willpower=15,
                base_magic_mana=5,
                base_experience_adjustment=400,
            ),
            PlayerRaceType(
                "Earea",
                "Enigmatic telepathic beings from the Whispering Plains. Earea are believed to be a hive-minded race, their origins shrouded in mystery. They possess potent mental abilities, allowing for communication and manipulation of thoughts, but are physically frail.",
                [
                    RaceAbilities.TELEPATHIC,
                ],
                base_hp=70,
                base_strength=7,
                base_agility=12,
                base_perception=16,
                base_willpower=14,
                base_magic_mana=15,
                base_experience_adjustment=300,
            ),
            PlayerRaceType(
                "Fae",
                "Graceful and ethereal beings from the enchanted Twilight Glades. Fae are deeply connected to the magical energies of the world, possessing an innate affinity for magic. They are often associated with nature and possess keen senses, though they can be physically delicate.",
                [
                    RaceAbilities.DARKVISION,
                    RaceAbilities.MAGIC,
                ],
                base_hp=80,
                base_strength=9,
                base_agility=14,
                base_perception=15,
                base_willpower=12,
                base_magic_mana=20,
                base_experience_adjustment=250,
            ),
            PlayerRaceType(
                "Goblin",
                "Small, green-skinned humanoids known for their cunning and scavenging skills. Goblins thrive in dark, cramped environments and are often seen as pests or nuisances. Though physically weak, they possess a knack for traps and trickery.",
                [
                    RaceAbilities.DARKVISION,
                ],
                base_hp=75,
                base_strength=8,
                base_agility=15,
                base_perception=13,
                base_willpower=10,
                base_magic_mana=5,
                base_experience_adjustment=200,
            ),
            PlayerRaceType(
                "Halfling",
                "Cheerful and stout folk from the rolling Greenmeadows. Halflings are renowned for their love of comfort, good food, and peaceful living. They are surprisingly agile and possess an uncanny knack for avoiding danger, often attributed to their inherent luck and sharp intuition.",
                [
                    RaceAbilities.HEIGHTENED_INTUITION,
                    RaceAbilities.HEIGHTENED_AGILITY,
                    RaceAbilities.LUCK,
                ],
                base_hp=90,
                base_strength=10,
                base_agility=16,
                base_perception=14,
                base_willpower=11,
                base_magic_mana=7,
                base_experience_adjustment=150,
            ),
            PlayerRaceType(
                "Half-Ogre",
                "The result of unions between humans and ogres, Half-Ogres inherit the brute strength of their ogre parentage. They are often ostracized by both societies, leading to a tough and resilient nature. While not as intelligent as humans, they possess a formidable willpower.",
                [
                    RaceAbilities.HEIGHTENED_STRENGTH2,
                    RaceAbilities.HEIGHTENED_WILL,
                ],
                base_hp=110,
                base_strength=19,
                base_agility=9,
                base_perception=9,
                base_willpower=16,
                base_magic_mana=4,
                base_experience_adjustment=450,
            ),
            PlayerRaceType(
                "Kobold",
                "Small, reptilian humanoids often dwelling in warrens or underground complexes. Kobolds are known for their cunning and agility, often relying on traps and ambushes to overcome their physical limitations. They have a strong sense of community and are fiercely loyal to their tribe.",
                [
                    RaceAbilities.HEIGHTENED_INTUITION,
                    RaceAbilities.HEIGHTENED_AGILITY,
                ],
                base_hp=75,
                base_strength=8,
                base_agility=17,
                base_perception=14,
                base_willpower=12,
                base_magic_mana=6,
                base_experience_adjustment=175,
            ),
            PlayerRaceType(
                "Nyrriss",
                "A race adapted to the treacherous swamps of Nyrriss. Nyriss are known for their resilience to poisons and diseases, as well as their highly developed senses of taste and smell. They are often reclusive and distrustful of outsiders.",
                [
                    RaceAbilities.POISON_IMMUNITY,
                    RaceAbilities.HEIGHTENED_TASTE,
                ],
                base_hp=95,
                base_strength=11,
                base_agility=13,
                base_perception=12,
                base_willpower=14,
                base_magic_mana=8,
                base_experience_adjustment=225,
            ),
            PlayerRaceType(
                "Orc",
                "Large, muscular humanoids with a reputation for ferocity and warfare. Orcs are known for their incredible strength and toughness, often favoring brute force over finesse. They possess a keen sense of smell and a strong tribal culture.",
                [
                    RaceAbilities.HEIGHTENED_STRENGTH,
                    RaceAbilities.HEIGHTENED_WILL,
                    RaceAbilities.HEIGHTENED_SMELL,
                ],
                base_hp=115,
                base_strength=17,
                base_agility=10,
                base_perception=11,
                base_willpower=15,
                base_magic_mana=6,
                base_experience_adjustment=350,
            ),
            PlayerRaceType(
                "Human",
                "Adaptable and versatile inhabitants of Illisurom. Humans are known for their capacity for learning and specialization, excelling in a wide range of fields. They lack the inherent strengths of other races but possess a drive and ambition that allows them to overcome their limitations.",
                [
                    RaceAbilities.SPECIALIZATION,
                ],
                base_hp=100,
                base_strength=12,
                base_agility=12,
                base_perception=12,
                base_willpower=12,
                base_magic_mana=10,
                base_experience_adjustment=0,
            ),
        ]
