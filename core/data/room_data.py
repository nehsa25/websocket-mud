from typing import Dict, List

from core.data.environment_data import EnvironmentData


class RoomData:
    environment: "EnvironmentData" = None

    def __init__(
        self,
        room_id: int,
        name: str,
        description: str,
        monsters: List[str],
        items: List[str],
        npcs: List[str],
        characters: List[str],
        exits: List[str],
        inside: bool = False,
        environment_name: str = "",
    ):
        self.room_id: int = room_id
        self.name = name
        self.description = description
        self.monsters = monsters
        self.items = items
        self.npcs = npcs
        self.characters = characters
        self.exits = exits
        self.inside = inside
        self.environment_name = environment_name

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert NPC to a dictionary."""
        return {
            "room_id": self.room_id,
            "name": self.name,
            "description": self.description,
            "monsters": self.monsters,
            "items": self.items,
            "npcs": self.npcs,
            "characters":  self.characters,
            "exits": self.exits,
            "inside": self.inside,
            "environment_name": self.environment_name,                  
        }
