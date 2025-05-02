from typing import Dict


class EnvironmentData:
    def __init__(
        self,
        name: str,
        description: str,
        spawn_monsters: bool = False,
        spawn_guards: bool = False,
    ):
        self.name = name
        self.description = description
        self.spawn_monsters = spawn_monsters
        self.spawn_guards = spawn_guards

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "spawn_monsters": self.spawn_monsters,
            "spawn_guards": self.spawn_guards,
        }
