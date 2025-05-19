import json
from typing import Dict, List, Optional


class MonsterData:
    def __init__(
        self,
        name: str,
        pronoun: str,
        alignment: str,  # e.g., "NEUTRAL"
        description: str,
        possible_adjectives: List[str],
        adjective_chance: int,
        respawn_rate_secs: Optional[int],
        room_id: Optional[int],
        player_race: str,
        player_class: str,
        level: int,
        wanders: bool,
        experience: int,
        money: int,
        title: Optional[str],
        attributes,
        directives: List[str],
        death_cry: str,
        entrance_cry: str,
        victory_cry: str,
        flee_cry: str,
    ):
        self.name = name
        self.pronoun = pronoun
        self.type = type
        self.alignment = alignment
        self.description = description
        self.possible_adjectives = possible_adjectives
        self.adjective_chance = adjective_chance
        self.respawn_rate_secs = respawn_rate_secs
        self.room_id = room_id
        self.player_race = player_race
        self.player_class = player_class
        self.level = level
        self.wanders = wanders
        self.attributes = attributes
        self.directives = directives
        self.experience = experience
        self.money = money
        self.title = title
        self.death_cry = death_cry
        self.entrance_cry = entrance_cry
        self.victory_cry = victory_cry
        self.flee_cry = flee_cry

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "pronoun": self.pronoun,
            "type": self.type,
            "alignment": self.alignment,
            "description": self.description,
            "possible_adjectives": json.dumps(self.possible_adjectives),
            "adjective_chance": self.adjective_chance,
            "respawn_rate_secs": self.respawn_rate_secs,
            "room_id": self.room_id,
            "player_race": self.player_race,
            "player_class": self.player_class,
            "level": self.level,
            "wanders": self.wanders,
            "attributes": self.attributes.to_dict() if self.attributes else None,
            "directives": self.directives,
            "experience": self.experience,
            "money": self.money,
            "title": self.title,
            "death_cry": self.death_cry,
            "entrance_cry": self.entrance_cry,
            "victory_cry": self.victory_cry,
            "flee_cry": self.flee_cry,
        }
    
