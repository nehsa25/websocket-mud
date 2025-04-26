from typing import Dict, List


class NpcData:
    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        interests: List[str],
        type: str,  # e.g., "SKELETON"
        wanders: bool,
    ):
        self.name = name
        self.title = title
        self.description = description
        self.interests = interests
        self.type = type
        self.wanders = wanders

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert NpcData to a dictionary."""
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "interests": self.interests,
            "type": self.type,
            "wanders": self.wanders,
        }
