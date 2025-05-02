import json
from typing import Dict, List, Optional


class NpcData:
    def __init__(
        self,
        name: str,
        type: str,
        room_id: Optional[int],
        pronoun: str,
        alignment: str,  # e.g., "NEUTRAL"
        attributes,
        experience: int,
        race_name: str,
        class_name: str,
        death_cry: str,
        entrance_cry: str,
        victory_cry: str,
        flee_cry: str,
        title: str,
        money: Optional[int],
        description: str,
        directives: List[str],
        wanders: bool,
        respawn_rate_secs: Optional[int],
    ):
        self.name = name
        self.type = type
        self.pronoun = pronoun
        self.alignment = alignment
        self.description = description
        self.title = title
        self.directives = directives
        self.room_id = room_id
        self.race_name = race_name
        self.class_name = class_name
        self.wanders = wanders
        self.experience = experience
        self.death_cry = death_cry
        self.entrance_cry = entrance_cry
        self.victory_cry = victory_cry
        self.flee_cry = flee_cry
        self.attributes = None
        self.money = money
        self.respawn_rate_secs = None
        self.attributes = attributes
        self.respawn_rate_secs = respawn_rate_secs

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert NpcData to a dictionary."""
        return {
            "name": self.name,
            "pronoun": self.pronoun,
            "type": self.type,
            "alignment": self.alignment,
            "description": self.description,
            "title": self.title,
            "directives": json.dumps(self.directives),
            "room_id": self.room_id,
            "race_name": self.race_name,
            "class_name": self.class_name,
            "wanders": self.wanders,
            "attributes": self.attributes.to_dict() if self.attributes else None,
            "money": self.money,
            "respawn_rate_secs": self.respawn_rate_secs,
            "experience": self.experience,
            "death_cry": self.death_cry,
            "entrance_cry": self.entrance_cry,
            "victory_cry": self.victory_cry,
            "flee_cry": self.flee_cry,            
        }

    def __repr__(self) -> str:
        return f"NpcData(name={self.name!r}, type={self.type!r})"
