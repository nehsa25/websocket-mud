import asyncio
import inspect
from random import randint
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Attack(Utility):
    logger = None
    description = "Attack something"
    command = "attack <target>"
    examples = [
        "a skeleton",
        "att skel",
        "attack skeleton"
    ]
    type = Utility.Commands.ATTACK
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Attack() class", self.logger)
        
    async def start_attack(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        room = world_state.rooms.rooms[player.room.id]

        # att skeleton
        wanted_monster = command.split(" ", 1)[1].lower()  # wanted_monster == skeleton

        # see if this monster is in the room.
        current_monster = None
        room_monsters = room.monsters
        for monster in room_monsters:
            monster_name = monster.name.lower().strip()
            monster_name_parts = monster_name.split(" ")
            for name in monster_name_parts:
                if name.startswith(wanted_monster) and monster.is_alive == True:
                    current_monster = monster
                    break

        if current_monster != None:
            if player.in_combat == None:
                for p in world_state.rooms.rooms[player.room.id].players:
                    if p.name == player.name:
                        await self.send_message(MudEvents.InfoEvent(f"You begin to attack {current_monster.name}!"), p.websocket)
                        p.in_combat = current_monster
                    else:
                        await self.send_message(MudEvents.InfoEvent(f"{player.name} begins to attack {current_monster.name}!"), p.websocket)

                # if you die and go to the crypt then your room id will change..
                while current_monster.hitpoints > 0 and player.room.id == world_state.rooms.rooms[player.room.id].id:
                    # determine attack damage
                    attack_potential = player.weapon.damage_potential

                    # for number of swings here
                    num_swings = 1
                    num_swings += int(player.attributes.agility / player.weapon.weight_class.value)

                    LogUtils.debug(f"We're going to swing {num_swings} times!", self.logger)

                    damage = 0
                    for x in range(0, num_swings):
                        LogUtils.debug(f"Swinging!", self.logger)
                        # attack monster
                        obj = attack_potential.split(
                            "d"
                        )  # obj = obj[0] == 1, obj[1] == 2
                        dice = int(obj[0])  # 1
                        damage_potential = int(obj[1])  # 2
                        damage_multipler = randint(0, damage_potential)
                        damage += dice * damage_multipler * player.attributes.strength

                    for p in world_state.rooms.rooms[player.room.id].players:
                        response = ""
                        if player.name == p.name:
                            if damage == 0:
                                response = f"You swing wildly and miss!"
                            else:
                                if num_swings == 1:
                                    response = f"You {player.weapon.verb} {current_monster.name} with your {player.weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"You {player.weapon.verb} {current_monster.name} {num_swings} times with your {player.weapon.name.lower()} for {str(damage)} damage!"
                                await self.send_message(MudEvents.InfoEvent(response), p.websocket)
                        else:
                            if damage == 0:
                                response = f"{player.name} swings wildly and misses!"
                            else:
                                if num_swings == 1:
                                    response = f"{player.name} {player.weapon.plural_verb} {current_monster.name} with their {player.weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"{player.name} {player.weapon.plural_verb} {current_monster.name} {num_swings} times with their {player.weapon.name.lower()} for {str(damage)} damage!"
                                await self.send_message(MudEvents.InfoEvent(response), p.websocket)

                    # subtract from monsters health
                    current_monster.hitpoints = current_monster.hitpoints - damage

                    if current_monster.hitpoints <= 0:
                        # set monster as dead
                        await current_monster.kill(world_state.rooms.rooms[player.room.id], self.logger)

                        for p in world_state.rooms.rooms[player.room.id].players:
                            if p.in_combat == current_monster:
                                # give experience
                                p.experience += current_monster.experience

                                # send defeat message
                                msg = f"You vanquished {current_monster.name}!<br>You received {current_monster.experience} experience."
                                await self.send_message(MudEvents.InfoEvent(msg), p.websocket)

                                # set combat back to none so we can fight someone else
                                p.in_combat = None

                                # show room
                                await world_state.show_room(player)

                        # add (Dead) to monster
                        current_monster.name = f"{current_monster.name} (Dead)"
                    else:
                        await asyncio.sleep(3)
            else:
                await self.send_message(MudEvents.ErrorEvent(f"You cannot attack {current_monster.name}.  You are already in combat with {player.in_combat.name}."), player.websocket)
        else:
            await self.send_message(MudEvents.ErrorEvent(f"{wanted_monster} is not a valid attack target."), player.websocket)
        world_state.rooms.rooms[player.room.id].monsters = room_monsters
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player


    async def execute(self, command, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        item = asyncio.create_task(
            self.start_attack(command, player, world_state)
        )
        
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return item