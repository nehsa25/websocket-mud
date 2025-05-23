from typing import Dict


class ExitData:
    def __init__(
        self,
        north: int = None,
        south: int = None,
        east: int = None,
        west: int = None,
        up: int = None,
        down: int = None,
        northeast: int = None,
        northwest: int = None,
        southeast: int = None,
        southwest: int = None       
    ):
        self.north: int = north
        self.south: int = south
        self.east: int = east
        self.west: int = west
        self.up: int = up
        self.down: int = down
        self.northeast: int = northeast
        self.northwest: int = northwest
        self.southeast: int = southeast
        self.southwest: int = southwest

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "north": self.north,
            "south": self.south,
            "east": self.east,
            "west": self.west,
            "up": self.up,
            "down": self.down,
            "northeast": self.northeast,
            "northwest": self.northwest,
            "southeast": self.southeast,
            "southwest": self.southwest
        }