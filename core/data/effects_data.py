from typing import Dict


class EffectsData:
    def __init__(
        self,
        keyword: str,
        description: str
    ):
        self.keyword = keyword
        self.description = description

    def __str__(self):
        return self.keyword

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "keyword": self.keyword,
            "description": self.description
        }
