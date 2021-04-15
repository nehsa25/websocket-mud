import sched, time
import asyncio
from random import randint

class Attack:
    @staticmethod
    def run_attack(monster, player):
        response = ""
        # response = f"{monster.name} prepares to attack you!<br>"

        # need to understand what damage monster can do        
        # roll dice
        obj = monster.damage.split('d')
        dice = int(obj[0])
        damage_potential = int(obj[1])
        damage_multipler = randint(1, damage_potential)
        damage = dice * damage_multipler

        response += f"{monster.name} has hit you for {str(damage)}!<br>"
        
        # return inflicted damage
        player.hitpoints = player.hitpoints - damage

        # update HP
        return response
