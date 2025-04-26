from typing import Dict, List, Optional


class DirectionData:
    def __init__(
        self,
        name: str,
        variations: List[str],
        opposite: Optional["DirectionData"] = None,
    ):
        self.name = name
        self.variations = variations
        self.opposite = opposite

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Direction to a dictionary."""
        return {
            "name": self.name,
            "variations": self.variations,
            "opposite": self.opposite,
        }
