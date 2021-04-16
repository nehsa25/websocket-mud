class Player:
    name = ""
    hitpoints = 0
    max_hitpoints = 0
    location = 0
    perception = 0
    inventory = []

    def __init__(self, name, hp, location, perception):
        self.name = name
        self.hitpoints = hp
        self.max_hitpoints = hp
        self.perception = perception
        self.location = location
