from typing import Dict


class CharacterData:
    def __init__(self, name, experience, level, money, sex, attributes, alignment, player_race, player_class, room_id):
        self.name: str = name
        self.experience: int = experience
        self.level: int = level
        self.money: int = money
        self.sex: str = sex
        self.attributes = attributes
        self.alignment: str = alignment
        self.player_race: str = player_race
        self.player_class: str = player_class
        self.room_id: int = room_id

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "experience": self.experience,
            "level": self.level,
            "money": self.money,
            "sex": self.sex,
            "attributes": self.attributes.to_dict(),
            "alignment": self.alignment,
            "player_race": self.player_race,
            "player_class": self.player_class,
            "room_id": self.room_id,
        }
