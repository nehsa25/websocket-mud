from typing import Dict, List


class RoomData:
    def __init__(
        self,
        room_id: int,
        name: str,
        environment: str,
        description: str,
        monsters: List[str],
        items: List[str],
        npcs: List[str],
        players: List[str],
        exits: List[str],
        inside: bool = False,
    ):
        self.room_id: int = room_id
        self.name = name
        self.environment = environment
        self.description = description
        self.monsters = monsters
        self.items = items
        self.npcs = npcs
        self.players = players
        self.exits = exits
        self.inside = inside

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert NPC to a dictionary."""
        return {
            "room_id": self.room_id,
            "name": self.name,
            "environment": self.environment,
            "description": self.description,
            "monsters": self.monsters,
            "items": self.items,
            "npcs": self.npcs,
            "players": self.players,
            "exits": self.exits,
            "inside": self.inside,
        }
