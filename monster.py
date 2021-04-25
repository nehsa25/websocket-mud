class Monster:
    name = ""
    hitpoints = 0
    damage = None
    experience = 0

    def __init__(self, name, hitpoints, damage_potential, experience):
        self.name = name
        self.hitpoints = hitpoints
        self.damage = damage_potential
        self.experience = experience
