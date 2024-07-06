import inspect
from items import Items
from log_utils import LogUtils
from room import Room
from utility import Utility


class TownSmee:
    monsters = None
    logger = None
    units = None
    rooms = None
    in_town = True
    name = "Town Smee"
    type = Utility.Share.EnvironmentTypes.TOWNSMEE

    def __init__(self, dirs, logger):
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing TownSmee() class", self.logger)
        self.monster_saturation = 0.5

        self.rooms = [
            Room(
                id=0,
                name=f"{self.name} - Town Square",
                inside=False,
                description="You are in the town square of the Town of Smee. It's a large open cobblestone area with a bronze water fountain. The fountain is in the shape of a large, ferocious dire wolf. Water jets from the foutain mouth in a small arc. There's a festive feeling to the area and people and wagons move with purpose in all directions.",
                exits=[
                    {"direction": dirs.west, "id": 9},  # moon road w
                    {"direction": dirs.northeast, "id": 22},
                    {"direction": dirs.southeast, "id": 21},
                    {"direction": dirs.northwest, "id": 20},
                    {"direction": dirs.southwest, "id": 23},
                    {"direction": dirs.east, "id": 10},  # moon road e
                    {"direction": dirs.north, "id": 11},  # sun road n
                    {"direction": dirs.south, "id": 12},  # sun road s
                ],
                items=[Items.helmet, Items.stick, Items.maul],
                monsters=[],
                npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=1,
                name=f"{self.name} - Inn",
                inside=True,
                description="You find yourself within a majestic inn. A worn, well-kept fireplace burned softly in the corner. There's a shelf with a small assortment of books and a prized map of the town and surrounding area stands on display but it is sealed behind glass to prevent touching.",
                exits=[
                    {"direction": dirs.south, "id": 9},
                    {"direction": dirs.up, "id": 3},
                ],
                npc_types=[Utility.Share.Npcs.INNKEEPER, Utility.Share.Npcs.PRINCESS],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=2,
                name=f"{self.name} - Sheriff's Office",
                inside=True,
                description="You are in the sheriff's office. A locked cell is in the corner of the Room. Currently, it is empty. A young bestraught woman is pleading and gusticulating to someone behind a small window.",
                exits=[
                    {"direction": dirs.east, "id": 11},  # sun road
                ],
                npc_types=[Utility.Share.Npcs.SHERIFF],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=3,
                name=f"{self.name} - Inn, second floor",
                inside=True,
                description="You are on the second floor of the inn. Rooms line the hallway.",
                exits=[
                    {"direction": dirs.up, "id": 4},  # inn, third floor
                    {"direction": dirs.down, "id": 1},  # inn, first floor
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=4,
                name=f"{self.name} - Inn, third floor",
                inside=True,
                description="You are on the third floor of the inn. Rooms line the hallway. A beautiful vase with daisies sit on a table in broad view.",
                exits=[
                    {"direction": dirs.down, "id": 3},  # inn, second floor
                ],
                hidden_items=[Items.helmet],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=5,
                name=f"{self.name} - Blacksmith",
                inside=True,
                npc_types=[Utility.Share.Npcs.BLACKSMITH],
                description="You are in the blacksmith's shop. An assortment of the blacksmiths wares are on display.",
                exits=[
                    {"direction": dirs.west, "id": 11},  # sun road
                    {"direction": dirs.east, "id": 6},  # back room
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=6,
                name=f"{self.name} - Blacksmith, back room",
                inside=True,
                description="You are in the blacksmith's back Room. A hot forge still burns smoldering coals.",
                exits=[
                    {"direction": dirs.west, "id": 5},
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=7,
                name=f"{self.name} - Market",
                inside=False,
                description="You are in the farmers market. Smells of exotic spices and searing meats are everywhere and loud vendors yell out their wares. The market is bustling with activity. Children and dogs are seen running everywhere with bright smiles. You even spot a Rite, a small azure and beige colored lizard two feet tall. Rites are harmless joyful creatures.",
                exits=[
                    {"direction": dirs.north, "id": 10},
                ],
                npc_types=[Utility.Share.Npcs.MERCHANT, Utility.Share.Npcs.THIEF],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=8,
                name=f"{self.name} - Armoury",
                inside=True,
                description="You are in the town armoury. A prominent case displays a beautifully crafted broadsword. The blade of the sword seems to glow slightly. It has a worn but well-kepted tightly-bound leather hilt. An assortment of other swords, shields, and armor are on display along the walls.",
                exits=[
                    {"direction": dirs.north, "id": 9},  # moon road
                ],
                npc_types=[Utility.Share.Npcs.ARMORER],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=9,
                name=f"{self.name} - Moon Road (West)---1",
                inside=False,
                description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": dirs.north, "id": 1},  # inn
                    {"direction": dirs.south, "id": 8},  # armoury
                    {"direction": dirs.east, "id": 0},  # town square
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=10,
                name=f"{self.name} - Moon Road (East)---3",
                inside=False,
                description=f"You are on one of the main thoroughfare of {Utility.Share.WORLD_NAME} running East and West directions. The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": dirs.west, "id": 0},  # town square
                    {"direction": dirs.south, "id": 7},  # market
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=11,
                name=f"{self.name} - Sun Road (North)---1",
                inside=False,
                description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": dirs.west, "id": 2},  # sheriff's office
                    {"direction": dirs.east, "id": 5},  # blacksmith
                    {"direction": dirs.south, "id": 0},  # town square
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=12,
                name=f"{self.name} - Sun Road (South)---1",
                inside=False,
                description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": dirs.north, "id": 0},  # town square
                    {"direction": dirs.south, "id": 13},
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=13,
                name=f"{self.name} - Sun Road (South)---2",
                inside=False,
                npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
                description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": dirs.north, "id": 12},  # town square
                    {"direction": dirs.south, "id": 14},  # blacksmith
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=14,
                name=f"{self.name} - Sun Road (South)---3",
                inside=False,
                description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": dirs.north, "id": 13},
                    {"direction": dirs.south, "id": 15},
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=15,
                name=f"{self.name} - Sun Road (South)---4",
                inside=False,
                description=f"You are on the main thoroughfare of {Utility.Share.WORLD_NAME} running North and South directions. The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": dirs.north, "id": 14},
                    {"direction": dirs.east, "id": 16},
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=16,
                name=f"{self.name} - Gallows Road (East)---1",
                inside=False,
                description=f"The road is more an alley than main thoroughfare. The road is narrow and the buildings are close together. Trash litters each wall and there's a sweet rot in the air, nearly visible to the eye.",
                npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
                exits=[
                    {"direction": dirs.west, "id": 15},
                    {"direction": dirs.east, "id": 17},
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=17,
                name=f"{self.name} - Gallows Road (East)---2",
                inside=False,
                description=f"The road is more an alley than main thoroughfare. The road is narrow and the buildings are close together. Trash litters each wall and there's a sweet rot in the air, nearly visible to the eye.",
                exits=[
                    {"direction": dirs.west, "id": 16},
                    {"direction": dirs.east, "id": 18},
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=18,
                name=f"{self.name} - The Gallows",
                inside=False,
                npc_types=[Utility.Share.Npcs.GUARD, Utility.Share.Npcs.GUARD],
                description=f"The road widens into a large gathering area. Sets of gallow line the road. A sign reads 'Next service in 3 days'. Admission is free but donations are accepted.",
                exits=[
                    {"direction": dirs.west, "id": 17},
                    {"direction": dirs.south, "id": 19},
                ],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=19,
                name=f"{self.name} - The Lower Quarter",
                inside=False,
                description=f"A gate with two guards stands before you. Each guard casually leans against halberds taller than they are. The gate is open and the guards are pleasantly chatting with each other whilst a long line of weary towns folk await admission into the city. A sign reads “1 copper entrance free. No exceptions.”",
                exits=[{"direction": dirs.north, "id": 18}],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=20,
                name=f"{self.name} - Mind Road (Northwest)---1",
                inside=False,
                description=f"Mind road, also known as Scholar's Avenue, is a narrow, gravel road that runs northwest to southeast in Smee, the road extends far to the southeast at the University of Smee.",
                exits=[{"direction": dirs.southeast, "id": 0}],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=21,
                name=f"{self.name} - Mind Road (SouthEast)---1",
                inside=False,
                description=f"Mind road, also known as Scholar's Avenue, is a narrow, gravel road that runs northwest, past the town square, to the University of Smee to the southeast.",
                exits=[{"direction": dirs.northwest, "id": 0}],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=22,
                name=f"{self.name} - Talent Road (NorthEast)---1",
                inside=False,
                description=f"Talent road is a cobblestoned street with an inclined elevation to the south.  This road has some of the finer merchants, inns, and shops in the town.  The street is lined with trees and the buildings are well kept.",
                exits=[{"direction": dirs.southwest, "id": 0}],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
            Room(
                id=23,
                name=f"{self.name} - Talent Road (SouthWest)---1",
                inside=False,
                description=f"Talent road is a cobblestoned street with an inclined elevation to the south.  This road has some of the finer merchants, inns, and shops in the town.  The street is lined with trees and the buildings are well kept.",
                exits=[{"direction": dirs.northeast, "id": 0}],
                environment=Utility.Share.EnvironmentTypes.TOWNSMEE,
                logger=logger
            ),
        ]
