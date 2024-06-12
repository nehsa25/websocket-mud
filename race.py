from enum import Enum


class SpecialAttributes:
    NightVision = False
    HeightenedSmell = False  # can see through adjacent rooms
    Luck = False
    SenseAware = False  # can track where someone has been
    MagicResistance = False
    Stealth = False
    SuperNaturalStealth = False
    Slow = False

    def SetAttributes(
        self,
        nightVision=False,
        heightenedSmell=False,
        luck=False,
        senseAware=False,
        magicResistance=False,
        stealth=False,
        superNaturalStealth=False,
        slow=False,
    ):
        self.NightVision = nightVision
        self.HeightenedSmell = heightenedSmell
        self.Luck = luck
        self.SenseAware = senseAware
        self.MagicResistance = magicResistance
        self.Stealth = stealth
        self.SuperNaturalStealth = superNaturalStealth
        self.Slow = slow


class Race:
    name = None
    description = None
    hp = 50
    strength = 10
    agility = 10
    perception = 100
    specialattributes = []

    def __init__(
        self, name, description, hp, strength, agility, perception, specialattributes
    ):
        self.name = name
        self.description = description
        self.hp += hp
        self.strength += strength
        self.agility += agility
        self.perception += perception
        self.specialattributes = specialattributes


class Races:
    class RacesEnum(Enum):
        HUMAN = 0,    
        HALFORC = 1
        KOBOLD = 2,
        GOBLIN = 3,
        HALFLING = 4,
        HALFOGRE = 5,
        FAE = 6,
        SNAKEPERSON = 7,
        ARGUNA = 8

    attributes = SpecialAttributes()
    human = Race(
        "Human",
        "A human of the world of Illisurom.",
        hp=0,
        strength=0,
        agility=0,
        perception=0,
        specialattributes=attributes.SetAttributes(),
    )
    halforc = Race(
        "Half-Orc",
        "A half-orc of the world of Illisurom.",
        hp=10,
        strength=20,
        agility=0,
        perception=10,
        specialattributes=attributes.SetAttributes(),
    )
    kobold = Race(
        "Kobold",
        "A member of the kobold race.  A diminished race but don't take them for granted!",
        hp=-5,
        strength=-15,
        agility=10,
        perception=60,
        specialattributes=attributes.SetAttributes(luck=True, stealth=True),
    )
    goblin = Race(
        "Goblin",
        "A vicious goblin of the world of Illisurom.",
        hp=-5,
        strength=0,
        agility=10,
        perception=60,
        specialattributes=attributes.SetAttributes(stealth=True),
    )
    halfling = Race(
        "Halfling",
        "A halfling of the world of Illisurom.",
        hp=-10,
        strength=-10,
        agility=20,
        perception=40,
        specialattributes=attributes.SetAttributes(luck=True, stealth=True),
    )
    halfogre = Race(
        "Halfogre",
        "A mighty half orge. You're strong but not very smart. Half-ogres have a natural resistance to magic.",
        hp=15,
        strength=15,
        agility=-20,
        perception=-40,
        specialattributes=attributes.SetAttributes(magicResistance=True),
    )
    fae = Race(
        "Fae",
        "A fairy! You're small and quick but not very strong. You have a natural resistance to magic.",
        hp=-20,
        strength=-10,
        agility=-10,
        perception=100,
        specialattributes=attributes.SetAttributes(
            senseAware=True, magicResistance=True, stealth=True
        ),
    )
    snakeperson = Race(
        "Nyrriss",
        "A snake person of the world of Illisurom.",
        hp=0,
        strength=5,
        agility=5,
        perception=25,
        specialattributes=attributes.SetAttributes(heightenedSmell=True, stealth=True),
    )
    arguna = Race(
        "Arguna",
        "A big lumbering race. You're slow but strong and hard to kill.",
        hp=100,
        strength=10,
        agility=0,
        perception=25,
        specialattributes=attributes.SetAttributes(
            senseAware=True, slow=True, magicResistance=True
        ),
    )


    def __iter__(self):
        for race in Races:
            yield race
