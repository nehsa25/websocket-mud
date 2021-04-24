class Monster:
    name = ""
    hitpoints = 0
    damage = None

    def __init__(self, name, hitpoints, damage_potential):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage_potential