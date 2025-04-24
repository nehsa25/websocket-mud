from typing import Dict, List, Optional


class MonsterType:
    def __init__(
        self,
        name: str,
        pronoun: str,
        type: str,  # e.g., "SKELETON"
        alignment: str,  # e.g., "NEUTRAL"
        description: str,
        possible_adjectives: List[str],
        adjective_chance: int,
        respawn_rate_secs: Optional[int],
        dead_epoch: Optional[int],
        wanders: bool,
        hitpoints: int,
        damage_potential: str,
        experience: int,
        money: int,
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
        self.dead_epoch = dead_epoch
        self.wanders = wanders
        self.hitpoints = hitpoints
        self.damage_potential = damage_potential
        self.experience = experience
        self.money = money
        self.death_cry = death_cry
        self.entrance_cry = entrance_cry
        self.victory_cry = victory_cry
        self.flee_cry = flee_cry

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert MonsterType to a dictionary."""
        return {
            "name": self.name,
            "pronoun": self.pronoun,
            "type": self.type,
            "alignment": self.alignment,
            "description": self.description,
            "possible_adjectives": self.possible_adjectives,
            "adjective_chance": self.adjective_chance,
            "respawn_rate_secs": self.respawn_rate_secs,
            "dead_epoch": self.dead_epoch,
            "wanders": self.wanders,
            "hitpoints": self.hitpoints,
            "damage_potential": self.damage_potential,
            "experience": self.experience,
            "money": self.money,
            "death_cry": self.death_cry,
            "entrance_cry": self.entrance_cry,
            "victory_cry": self.victory_cry,
            "flee_cry": self.flee_cry,
        }
