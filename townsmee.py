from environments import Environments
from items import Items
from log_utils import LogUtils
from room import Room
from unit import Unit
from utility import Utility


class TownSmeeUnitFactory:
    utility = None
    sheriff = None
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
        self.units.append(sheriff)


class TownSmee(Utility):
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
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=1,
                name=f"{self.name} - Inn",
                description= "You find yourself within a majestic inn.  The smell of food and wine permeates the air.  A worn, well-kept fireplace burned softly in the corner.  There's a shelf with a small assortment of books.",
                exits=[
                    {"direction": Room.dirs.south, "id": 9},
                    {"direction": Room.dirs.up, "id": 3},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=2,
                name=f"{self.name} - Sheriff's Office",
                description="You are in the sheriff's office.  ",
                exits=[
                    {"direction": Room.dirs.east, "id": 11},  # sun road
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=3,
                name=f"{self.name} - Inn, second floor",
                description="You are on the second floor of the inn.  Rooms line the hallway.",
                exits=[
                    {"direction": Room.dirs.up, "id": 4}, # inn, third floor
                    {"direction": Room.dirs.down, "id": 1},  # inn, first floor
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=4,
                name=f"{self.name} - Inn, third floor",
                description="You are on the third floor of the inn.  Rooms line the hallway.",
                exits=[
                    {"direction": Room.dirs.down, "id": 3},  # inn, second floor
                ],
                hidden_items=[Items.helmet],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=5,
                name=f"{self.name} - Blacksmith",
                description="You are in the blacksmith's shop.",
                exits=[
                    {"direction": Room.dirs.west, "id": 8},  # town square
                    {"direction": Room.dirs.east, "id": 6},  # back room
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=6,
                name=f"{self.name} - Blacksmith, back room",
                description="You are in the blacksmith's back room.",
                exits=[
                    {"direction": Room.dirs.west, "id": 5},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=7,
                name=f"{self.name} - Market",
                description="You are in the farmers market.",
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
                    {"direction": Room.dirs.north, "id": 0} # town square
                ],
                environment=Environments.TOWNSMEE,
            ),
        ]
        self.unitfactory = TownSmeeUnitFactory(self.rooms, logger)

    # self.rooms = self.rooms
    # self.units = self.units
