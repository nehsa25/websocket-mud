from utilities.log_telemetry import LogTelemetryUtility
from directions.down import Down
from directions.east import East
from directions.north import North
from directions.northeast import NorthEast
from directions.northwest import NorthWest
from directions.south import South
from directions.southeast import SouthEast
from directions.southwest import SouthWest
from directions.up import Up
from directions.west import West


class Directions:
    logger = None
    up = None
    down = None
    north = None
    south = None
    east = None
    west = None
    northeast = None
    northwest = None
    southeast = None
    southwest = None
    directions = []

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing direction() class")
        
        self.up = Up()
        self.down = Down()
        self.north = North()
        self.south = South()
        self.east = East()
        self.west = West()
        self.northeast = NorthEast()
        self.northwest = NorthWest()
        self.southeast = SouthEast()
        self.southwest = SouthWest()

        # build our list of possible directions
        self.directions.append(self.up)
        self.directions.append(self.down)
        self.directions.append(self.north)
        self.directions.append(self.south)
        self.directions.append(self.east)
        self.directions.append(self.west)
        self.directions.append(self.northeast)
        self.directions.append(self.northwest)
        self.directions.append(self.southeast)
        self.directions.append(self.southwest)

    def is_valid_direction(self, direction):
        foundness = [x for x in self.directions if direction.lower() in x.variations]
        return len(foundness) > 0

    async def get_opposite_direction(self, direction):
        opp_direction = None
        for directions in Directions.opp_directions:
            if direction in directions[0]:
                opp_direction = directions[1]
                break
            elif direction in directions[1]:
                opp_direction = directions[0]
                break
        return opp_direction

    async def get_friendly_name(self, direction):
        foundness = [x for x in self.directions if direction.lower() in x.variations]
        return foundness[0].name.lower()
