from typing import Dict


class PlayerData:
    def __init__(self, name, role, experience, level, money, pronoun, attributes, alignment, player_race, player_class, room_id):
        self.name: str = name
        self.role: str = role
        self.experience: int = experience
        self.level: int = level
        self.money: int = money
        self.pronoun: str = pronoun
        self.attributes = attributes
        self.alignment: str = alignment
        self.player_race: str = player_race
        self.player_class: str = player_class
        self.room_id = room_id

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "experience": self.experience,
            "level": self.level,
            "money": self.money,
            "pronoun": self.pronoun,
            "attributes": self.attributes.to_dict(),
            "alignment": self.alignment,
            "player_race": self.player_race,
            "player_class": self.player_class,
            "room_id": self.room_id,
        }
