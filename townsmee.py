from environments import Environments
from items import Items
from log_utils import LogUtils
from monsters import Monsters
from room import Room
from unit import Unit
from utility import Utility


class TownSmeeUnitFactory:
    utility = None
    sheriff = None
    inn_keeper = None
    unit_factory = None
    units = []
    logger = None

    def __init__(self, rooms, logger):
        self.logger = logger
        LogUtils.debug("Initializing TownSmeeUnitFactory() class", self.logger)
        self.utility = Utility(self.logger)
        self.unit_factory = Unit(self.logger)
        sheriff = self.unit_factory.generate_unit(
            title="Sheriff",
            name=self.utility.generate_name(),
            hp=250,
            strength=10,
            agility=30,
            location=self.utility.generate_location(rooms),
            description="The sheriff of Town Smee.  The sheriff is a slender, man with a mustache.  He has a menacing cudgel at his waist.",
            perception=250,
        ) 

        inn_keeper = self.unit_factory.generate_unit(
            title= ""
            name= "Jared the Inn-keeper",
            hp=250,
            strength=10,
            agility=30,
            location=self.utility.generate_location(rooms),
            description="""A slightly obese man with short blonde hair and a sickly pale face. He is dressed in the usual inn keeper garb. 
            A lime green button up shirt, old grey breeches with red patches, and a grease stained apron. Jared is well beloved by the residents 
            town Smee due to his charming stories and friendly additude.""",
            perception=250,
        ) 
        self.units.append(sheriff)



class TownSmee(Utility):
    monsters = None
    logger = None
    unitfactory = None
    rooms = None
    name = "Town Smee"
    world_name = ""
    type = Environments.TOWNSMEE

    def __init__(self, world_name, logger):
        self.logger = logger
        LogUtils.debug("Initializing TownSmee() class", self.logger)
        self.world_name = world_name
        self.monsters = Monsters(self.logger)
        self.rooms = [
            Room(
                id=0,
                name=f"{self.name} - Town Square",
                description="You are in the town square.  A large open cobblestone area with a fountain is in the center.",
                exits=[
                    {"direction": Room.dirs.west, "id": 9},  # moon road
                    {"direction": Room.dirs.east, "id": 10},  # moon road
                    {"direction": Room.dirs.south, "id": 12},  
                    {"direction": Room.dirs.north, "id": 11},  # sun road
                ],
                items=[Items.helmet, Items.stick, Items.maul],
                monsters=[
                    self.monsters.get_skeleton(),
                    self.monsters.get_skeleton(),
                    self.monsters.get_zombie(),
                    self.monsters.get_ghoul()
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=1,
                name=f"{self.name} - Inn",
                description= "You find yourself within a majestic inn.  A worn, well-kept fireplace burned softly in the corner.  There's a shelf with a small assortment of books and a prized map of the town and surrounding area stands on display but it is sealed behind glass to prevent touching.",
                exits=[
                    {"direction": Room.dirs.south, "id": 9},
                    {"direction": Room.dirs.up, "id": 3},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=2,
                name=f"{self.name} - Sheriff's Office",
                description="You are in the sheriff's office.  A locked cell is in the corner of the room.  Currently, it is empty.",
                exits=[
                    {"direction": Room.dirs.east, "id": 11},  # sun road
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=3,
                name=f"{self.name} - Inn, second floor",
                description="You are on the second floor of the inn. Rooms line the hallway.",
                exits=[
                    {"direction": Room.dirs.up, "id": 4}, # inn, third floor
                    {"direction": Room.dirs.down, "id": 1},  # inn, first floor
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=4,
                name=f"{self.name} - Inn, third floor",
                description="You are on the third floor of the inn.  Rooms line the hallway. A beautiful vase with daisies sit on a table in broad view.",
                exits=[
                    {"direction": Room.dirs.down, "id": 3},  # inn, second floor
                ],
                hidden_items=[Items.helmet],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=5,
                name=f"{self.name} - Blacksmith",
                description="You are in the blacksmith's shop.  An assortment of the blacksmiths wares are on display.",
                exits=[
                    {"direction": Room.dirs.west, "id": 12},  # sun road
                    {"direction": Room.dirs.east, "id": 6},  # back room
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=6,
                name=f"{self.name} - Blacksmith, back room",
                description="You are in the blacksmith's back room.  A hot forge still burns smoldering coals.",
                exits=[
                    {"direction": Room.dirs.west, "id": 5},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=7,
                name=f"{self.name} - Market",
                description="You are in the farmers market.  Loud vendors yell out their wares.  The market is bustling with activity.  Children and dogs are seen everywhere with bright smiles.",
                exits=[
                    {"direction": Room.dirs.north, "id": 10},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=8,
                name=f"{self.name} - Armoury",
                description="You are in the town armoury.",
                exits=[
                    {"direction": Room.dirs.north, "id": 9},  # moon road
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=9,
                name=f"{self.name} - Moon Road (West)---1",
                description=f"You are on one of the main thoroughfare of {self.world_name} running East and West directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.north, "id": 1},  # inn
                    {"direction": Room.dirs.south, "id": 8},  # armoury
                    {"direction": Room.dirs.east, "id": 0},  # town square
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=10,
                name=f"{self.name} - Moon Road (East)---1",
                description=f"You are on one of the main thoroughfare of {self.world_name} running East and West directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.west, "id": 0}, # town square
                    {"direction": Room.dirs.south, "id": 7} # market
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=11,
                name=f"{self.name} - Sun Road (North)---1",
                description=f"You are on the main thoroughfare of {self.world_name} running North and South directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 0} # town square
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=12,
                name=f"{self.name} - Sun Road (South)---1",
                description=f"You are on the main thoroughfare of {self.world_name} running North and South directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.north, "id": 0}, # town square
                    {"direction": Room.dirs.east, "id": 5} # blacksmith
                ],
                environment=Environments.TOWNSMEE,
            ),
        ]
        self.unitfactory = TownSmeeUnitFactory(self.rooms, logger)

    # self.rooms = self.rooms
    # self.units = self.units
