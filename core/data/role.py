from typing import Dict

class RoleData:
    damage = str  # this is a 1d6 type string
    quality = int
    speed = int

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
        return {
            "name": self.name,
            "description": self.description,
        }
    def __repr__(self):
        return f"RoleData(name={self.name!r}, description={self.description!r})"