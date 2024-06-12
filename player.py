from items import Items


class Player:
    name = None
    level = 1
    hitpoints = 0
    max_hitpoints = 0
    location = 0
    strength = 0
    agility = 0
    perception = 0
    experience = 0
    resting = False
    in_combat = None
    inventory = [Items.book, Items.cloth_pants]
    money = []
    websocket = None

    def __init__(self, hp, strength, agility, location, perception):
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.location = location
