from typing import Dict, List


class RoomType:
    def __init__(
        self,
        name: str,
        description: str,
        monsters: List[str],
        items: List[str],
        npcs: List[str],
        players: List[str],
        exits: List[str],
        inside: bool = False,
    ):
        self.name = name
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
            "name": self.name,
            "description": self.description,
            "monsters": self.monsters,
            "items": self.items,
            "npcs": self.npcs,
            "players": self.players,
            "exits": self.exits,
            "inside": self.inside,
        }
