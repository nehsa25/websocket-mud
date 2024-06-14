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
        LogUtils.info("Initializing TownSmeeUnitFactory() class", self.logger)
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

    def __init__(self, logger):
        self.logger = logger
        LogUtils.info("Initializing TownSmee() class", self.logger)        
        self.rooms = [
            Room(
                id=0,
                name="Town Smee - Inn",
                description="You are in a majestic inn.  The grandest building in town.  A three-storied building with a yellow roof.",
                exits=[
                    {"direction": Room.dirs.east, "id": 1},
                    {"direction": Room.dirs.up, "id": 2},
                ],
                environment=Room.Environments.TOWNSMEE,
            ),
            Room(
                id=1,
                name="Town Smee - Town Square",
                description="You are in the town square.  A large open cobblestone area with a fountain is in the center.",
                exits=[
                    {"direction": Room.dirs.west, "id": 0},
                    {"direction": Room.dirs.east, "id": 2},
                ],
                environment=Room.Environments.TOWNSMEE,
            ),
            Room(
                id=2,
                name="Town Smee - Sheriff's Office",
                description="You are in the sheriff's office.  ",
                exits=[
                    {"direction": Room.dirs.west, "id": 1},
                ],
                environment=Room.Environments.TOWNSMEE,
            ),
            Room(
                id=3,
                name="Town Smee - Inn, second floor",
                description="You are on the second floor of the inn.  Rooms line the hallway.",
                exits=[
                    {"direction": Room.dirs.up, "id": 4},
                    {"direction": Room.dirs.down, "id": 0},
                ],
                environment=Room.Environments.TOWNSMEE,
            ),
            Room(
                id=4,
                name="Town Smee - Inn, third floor",
                description="You are on the third floor of the inn.  Rooms line the hallway.",
                exits=[
                    {"direction": Room.dirs.down, "id": 3},
                ],
                hidden_items=[Items.helmet],
                environment=Room.Environments.TOWNSMEE,
            ),
        ]

        self.unitfactory = TownSmeeUnitFactory(self.rooms, logger)
        
    # self.rooms = self.rooms
    # self.units = self.units
