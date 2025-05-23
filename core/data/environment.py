from typing import List

class EnvironmentData:
    def __init__(self, environment_id: str, name: str, description: str = "", rooms: List[str] = None):
        self.environment_id = environment_id
        self.name = name
        self.description = description
        self.rooms = rooms if rooms is not None else []

    def __repr__(self):
        return f"<Environment id='{self.environment_id}' name='{self.name}'>"

    def add_room(self, room_id: str):
        """Adds a room ID to the list of rooms in this environment."""
        if room_id not in self.rooms:
            self.rooms.append(room_id)

    def remove_room(self, room_id: str):
        """Removes a room ID from the list of rooms in this environment."""
        if room_id in self.rooms:
            self.rooms.remove(room_id)