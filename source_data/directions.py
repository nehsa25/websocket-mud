from game.interfaces.source_data import SourceInterface
from class_types.direction_type import DirectionType


class DirectionsSource(SourceInterface):
    """
    This class is used to represent the source data for directions for
    initalization of the database.
    """

    def get_data(self):
        up = DirectionType(
            name="Up",
            variations=[("up", "u")],
            opposite=None,
        )
        down = DirectionType(
            name="Down",
            variations=[("down", "d")],
            opposite=up,
        )
        down.opposite = up
        east = DirectionType(
            name="East",
            variations=[("east", "e")],
            opposite=None,
        )
        west = DirectionType(
            name="West",
            variations=[("west", "w")],
            opposite=east,
        )
        east.opposite = west

        north = DirectionType(
            name="North",
            variations=[("north", "n")],
            opposite=None,
        )
        south = DirectionType(
            name="South",
            variations=[("south", "s")],
            opposite=north,
        )
        north.opposite = south
        northeast = DirectionType(
            name="Northeast",
            variations=[("northeast", "ne")],
            opposite=None,
        )
        northwest = DirectionType(
            name="Northwest",
            variations=[("northwest", "nw")],
            opposite=northeast,
        )
        northeast.opposite = northwest
        southeast = DirectionType(
            name="Southeast",
            variations=[("southeast", "se")],
            opposite=None,
        )
        southwest = DirectionType(
            name="Southwest",
            variations=[("southwest", "sw")],
            opposite=southeast,
        )
        southeast.opposite = southwest

        return [
            up,
            down,
            east,
            west,
            north,
            south,
            northeast,
            northwest,
            southeast,
            southwest,
        ]
