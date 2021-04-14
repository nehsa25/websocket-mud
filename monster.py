class Monster:
    name = ""
    hp = 0
    damage = None

    def __init__(self, name, health, damage_potential):
        self.name = name
        self.hp = health
        self.damage = damage_potential
