from log_utils import LogUtils
from class_types.down import Down
from class_types.east import East
from class_types.north import North
from class_types.northeast import NorthEast
from class_types.northwest import NorthWest
from class_types.south import South
from class_types.southeast import SouthEast
from class_types.southwest import SouthWest
from class_types.up import Up
from class_types.west import West
from utility import Utility

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
    
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing direction() class", self.logger)
        
        self.up = Up(self.logger)
        self.down = Down(self.logger)
        self.north = North(self.logger)
        self.south = South(self.logger)
        self.east = East(self.logger)
        self.west = West(self.logger)
        self.northeast = NorthEast(self.logger)
        self.northwest = NorthWest(self.logger)
        self.southeast = SouthEast(self.logger)
        self.southwest = SouthWest(self.logger)
        
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
        
    def get_opposite_direction(direction):
        opp_direction = None
        for directions in Utility.Share.MudDirections.opp_directions:
            if direction in directions[0]:
                opp_direction = directions[1]
                break
            elif direction in directions[1]:
                opp_direction = directions[0]
                break
        return opp_direction

    def get_friendly_name(direction):
        friendly_name = None
        for pretty_direction in Utility.Share.MudDirections.pretty_directions:
            if direction in pretty_direction:
                friendly_name = pretty_direction[1].capitalize()
                break
        return friendly_name
