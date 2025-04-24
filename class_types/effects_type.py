from typing import Dict


class EffectsType:
    def __init__(
        self,
        keyword: str,
        type: str
    ):
        self.keyword = keyword
        self.type = type

    def __str__(self):
        return self.keyword

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "keyword": self.keyword,
            "type": self.type
        }
