import pydot
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


class TownSmee:
    logger = None
    unitfactory = None
    rooms = None
    name = "Town Smee"
    world_name = "";

    def __init__(self, world_name, logger):
        self.logger = logger
        LogUtils.debug("Initializing TownSmee() class", self.logger)       
        self.world_name = world_name
        self.rooms = [
            Room(
                id=0,
                name="Town Smee - Inn",
                description="You are in a majestic inn.  The grandest building in town.  A three-storied building with a yellow roof.",
                exits=[
                    {"direction": Room.dirs.east, "id": 1},
                    {"direction": Room.dirs.up, "id": 3},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=1,
                name="Town Smee - Town Square",
                description="You are in the town square.  A large open cobblestone area with a fountain is in the center.",
                exits=[
                    {"direction": Room.dirs.west, "id": 0},
                    {"direction": Room.dirs.east, "id": 2},
                    {"direction": Room.dirs.south, "id": 7},
                    {"direction": Room.dirs.north, "id": 17},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=2,
                name="Town Smee - Sheriff's Office",
                description="You are in the sheriff's office.  ",
                exits=[
                    {"direction": Room.dirs.west, "id": 1},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=3,
                name="Town Smee - Inn, second floor",
                description="You are on the second floor of the inn.  Rooms line the hallway.",
                exits=[
                    {"direction": Room.dirs.up, "id": 4},
                    {"direction": Room.dirs.down, "id": 0},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=4,
                name="Town Smee - Inn, third floor",
                description="You are on the third floor of the inn.  Rooms line the hallway.",
                exits=[
                    {"direction": Room.dirs.down, "id": 3},
                ],
                hidden_items=[Items.helmet],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=5,
                name="Town Smee - Blacksmith",
                description="You are in the blacksmith's shop.",
                exits=[
                    {"direction": Room.dirs.east, "id": 1},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=6,
                name="Town Smee - Blacksmith, back room",
                description="You are in the blacksmith's back room.",
                exits=[
                    {"direction": Room.dirs.west, "id": 5},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=7,
                name="Town Smee - Market",
                description="You are in the farmers market.",
                exits=[
                    {"direction": Room.dirs.north, "id": 1},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=8,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 9},
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=9,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 10},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=10,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 11},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=11,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 12},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=12,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 13},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=13,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 14},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=14,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 15},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=15,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 16},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=16,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.south, "id": 17},
                    {"direction": Room.dirs.north, "id": 16}
                ],
                environment=Environments.TOWNSMEE,
            ),
            Room(
                id=17,
                name="Town Smee - Sun Road",
                description=f"You are on the main thoroughfare of {self.world_name} running north and south directions.  The street is broad, allowing for two wagons to pass each other.",
                exits=[
                    {"direction": Room.dirs.north, "id": 16},
                    {"direction": Room.dirs.south, "id": 1},
                ],
                environment=Environments.TOWNSMEE,
            ),
        ]
        self.unitfactory = TownSmeeUnitFactory(self.rooms, logger)
        
    # self.rooms = self.rooms
    # self.units = self.units
