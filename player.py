class Player:
    name = ""
    hitpoints = 0
    max_hitpoints = 0
    location = 0
    strength = 0
    dexerity = 0
    perception = 0
    inventory = []

    def __init__(self, name, hp, strength, dex, location, perception):
        self.name = name
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.strength = strength
        self.dexerity = dex
        self.perception = perception
        self.location = location
