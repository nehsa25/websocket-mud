import asyncio
from random import randint
from core.events.error import ErrorEvent
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
from core.enums.commands import CommandEnum


class Attack:
    logger = None
    description = "Attack something"
    command = "attack <target>"
    examples = ["a skeleton", "att skel", "attack skeleton"]
    type = CommandEnum.ATTACK

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Attack() class")

    async def start_attack(self, command, player, world_state):
        self.logger.debug("enter")

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
                if name.startswith(wanted_monster) and monster.is_alive is True:
                    current_monster = monster
                    break

        if current_monster is not None:
            if player.in_combat is None:
                for p in world_state.rooms.rooms[player.room.id].players:
                    if p.name == player.name:
                        await InfoEvent(f"You begin to attack {current_monster.name}!").send(p.websocket)
                        p.in_combat = current_monster
                    else:
                        await InfoEvent(f"{player.name} begins to attack {current_monster.name}!").send(p.websocket)

                # if you die and go to the crypt then your room id will change..
                while current_monster.hitpoints > 0 and player.room.id == world_state.rooms.rooms[player.room.id].id:
                    attack_potential = player.weapon.damage_potential  # determine attack damage

                    # for number of swings here
                    num_swings = 1
                    num_swings += int(player.attributes.dexterity / player.weapon.weight_class.value)

                    self.logger.debug(f"We're going to swing {num_swings} times!")

                    damage = 0
                    for x in range(0, num_swings):
                        self.logger.debug("Swinging!")
                        # attack monster
                        obj = attack_potential.split("d")  # obj = obj[0] == 1, obj[1] == 2
                        dice = int(obj[0])  # 1
                        damage_potential = int(obj[1])  # 2
                        damage_multipler = randint(0, damage_potential)
                        damage += dice * damage_multipler * player.attributes.strength

                    for p in world_state.rooms.rooms[player.room.id].players:
                        response = ""
                        if player.name == p.name:
                            if damage == 0:
                                response = "You swing wildly and miss!"
                            else:
                                if num_swings == 1:
                                    response = f"You {player.weapon.verb} {current_monster.name} with your {player.weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"You {player.weapon.verb} {current_monster.name} {num_swings} times with your {player.weapon.name.lower()} for {str(damage)} damage!"
                                await InfoEvent(response).send(p.websocket)
                        else:
                            if damage == 0:
                                response = f"{player.name} swings wildly and misses!"
                            else:
                                if num_swings == 1:
                                    response = f"{player.name} {player.weapon.plural_verb} {current_monster.name} with their {player.weapon.name.lower()} for {str(damage)} damage!"
                                else:
                                    response = f"{player.name} {player.weapon.plural_verb} {current_monster.name} {num_swings} times with their {player.weapon.name.lower()} for {str(damage)} damage!"
                                await InfoEvent(response).send(p.websocket)

                    # subtract from monsters health
                    current_monster.hitpoints = current_monster.hitpoints - damage

                    if current_monster.hitpoints <= 0:
                        # set monster as dead
                        await current_monster.kill(world_state.rooms.rooms[player.room.id])

                        for p in world_state.rooms.rooms[player.room.id].players:
                            if p.in_combat == current_monster:
                                # give experience
                                p.experience += current_monster.experience

                                # send defeat message
                                msg = f"You vanquished {current_monster.name}!<br>You received {current_monster.experience} experience."
                                await InfoEvent(msg).send(p.websocket)

                                # set combat back to none so we can fight someone else
                                p.in_combat = None

                                # show room
                                await world_state.show_room(player)

                        # add (Dead) to monster
                        current_monster.name = f"{current_monster.name} (Dead)"
                    else:
                        await asyncio.sleep(3)
            else:
                await ErrorEvent(
                    f"You cannot attack {current_monster.name}.  You are already in combat with {player.in_combat.name}."
                ).send(player.websocket)
        else:
            await ErrorEvent(f"{wanted_monster} is not a valid attack target.").send(player.websocket)
        world_state.rooms.rooms[player.room.id].monsters = room_monsters
        self.logger.debug("exit")
        return player

    async def execute(self, command, player, world_state):
        self.logger.debug("enter")
        item = asyncio.create_task(self.start_attack(command, player, world_state))

        self.logger.debug("exit")
        return item
