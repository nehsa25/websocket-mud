from typing import Dict


class AligntmentsData:
    def __init__(
        self,
        name: str,
        description: str
    ):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "name": self.name,
            "description": self.description
        }
