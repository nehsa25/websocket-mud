from __future__ import annotations
from abc import ABC
from core.data.attributes_data import AttributesData


class CharacterInterface(ABC):
    name: str
    firstname: str
    lastname: str
    experience: int
    level: int
    money: int
    sex: str
    attributes: "AttributesData"  # the quotes makes this a foward reference (it won't be evaluated until later thus preventing circular imports)
    alignment: str
    player_race: str
    player_class: str
    room_id: int
    eye_color: str
    eye_brow: str
    body_type: str
    hair_color: str
    hair_style: str
