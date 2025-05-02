from core.data.direction_data import DirectionData
from core.interfaces.source_data import SourceInterface


class DirectionsSource(SourceInterface):
    """
    This class is used to represent the source data for directions for
    initalization of the database.
    """

    def get_data(self):
        up = DirectionData(
            name="Up",
            variations=["up", "u"],
            opposite=None,
        )
        down = DirectionData(
            name="Down",
            variations=["down", "d"],
            opposite=up,
        )
        up.opposite = down # update our up direction to point to down

        east = DirectionData(
            name="East",
            variations=["east", "e"],
            opposite=None,
        )
        west = DirectionData(
            name="West",
            variations=["west", "w"],
            opposite=east,
        )
        east.opposite = west

        north = DirectionData(
            name="North",
            variations=["north", "n"],
            opposite=None,
        )
        south = DirectionData(
            name="South",
            variations=["south", "s"],
            opposite=north,
        )
        north.opposite = south
        northeast = DirectionData(
            name="Northeast",
            variations=["northeast", "ne"],
            opposite=None,
        )
        northwest = DirectionData(
            name="Northwest",
            variations=["northwest", "nw"],
            opposite=northeast,
        )
        northeast.opposite = northwest
        southeast = DirectionData(
            name="Southeast",
            variations=["southeast", "se"],
            opposite=None,
        )
        southwest = DirectionData(
            name="Southwest",
            variations=["southwest", "sw"],
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
