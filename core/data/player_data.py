from typing import Dict


class PlayerData:
    def __init__(
        self, firstname, lastname, email, role, pin, salt
    ):
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.role: str = role
        self.email: str = email
        self.pin: str = pin
        self.salt: str = salt

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "role": self.role,
            "email": self.email,
            "pin": self.pin,
            "salt": self.salt,
        }
