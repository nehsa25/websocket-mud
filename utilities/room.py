import random


class RoomUtility:
    @staticmethod
    def generate_location(rooms):
        id = random.choice(rooms).id
        return id
