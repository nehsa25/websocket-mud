from copy import deepcopy
from enum import Enum
import inspect
import random
from log_utils import LogUtils
from monster import Monster
from mudevent import MudEvents
from utility import Utility
    
class Battle(Utility):
    class BattleState(Enum):
        CHECKING = 0
        STARTING = 1
        INPROGRESS = 2
        COMPLETED = 3
        NONSTART = 4
        RECORDED = 5

    logger = None
    room = None
    rounds = []
    state = None

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug(f"Initializing Battle() class", self.logger) 
        self.state = Battle.BattleState.CHECKING
        
    async def stop_battle(self, battle, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        await self.alert_room("The battle has ended!", battle.room)
        self.rooms = await world.rooms.update_room(battle.room, world)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return battle
 
class CombatRound(Utility):
    logger = None
    monsters = []
    room = None
    damage_taken = 0
    damage_dealt = 0
    
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug(f"Initializing CombatRound() class", self.logger)
        
class Battles(Utility):
    battles = []
    logger = None
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug(f"Initializing Battles() class", self.logger)

    # every two seconds this method is called
    # it will check to see if the monster is still in combat
    async def run_combat_round(self, battle, players, world=None):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        
        if len(players.players) == 0:
            LogUtils.info(f"{method_name}: No players in world, stopping all battles", self.logger)
            if battle is not None and battle.state == Battle.BattleState.CHECKING:
                battle.state = Battle.BattleState.NONSTART
            else:
                battle.state = Battle.BattleState.COMPLETED
            return battle, world
        
        if battle is None:
            battle = Battle(self.logger)   
            LogUtils.info(
                f"{method_name}: A new battle has started", self.logger
            )
            
        # if monster is not attacking anyone, pick someone
        for p in players.players:
            round = CombatRound(self.logger)  
            if battle.room is None:
                LogUtils.info(f"{method_name}: Setting battle room: {p.room.name}", self.logger)
                battle.room = p.room
            if battle.state  == Battle.BattleState.CHECKING:                      
                for monster in battle.room.monsters:
                    if monster.is_alive == True:
                        LogUtils.debug(f'{method_name}: Monster "{monster.name}" is alive', self.logger)
                    else:
                        LogUtils.debug(f'{method_name}: Monster "{monster.name}" is dead.  Skipping.', self.logger)
                        continue
                    
                    if monster.alignment != Monster.Alignment.NEUTRAL:
                        monster.in_combat = random.choice(battle.room.players)
                        LogUtils.debug(f'{method_name}: "{monster.name}" is not attacking anyone.  Now attacking {monster.in_combat.name}', self.logger)   
                        await self.alert_room(f"{monster.name} stirs.", battle.room, event_type=MudEvents.InfoEvent)                      
                        if monster.in_combat == p:
                            await self.send_message(MudEvents.AttackEvent(f"{monster.name} prepares to attack you!"), p.websocket)
                        else:
                            await self.alert_room(f"{monster.name} prepares to attack {monster.in_combat.name}.", battle.room, event_type=MudEvents.InfoEvent, exclude_player=True, player=p)
                battle.state = Battle.BattleState.STARTING
            elif battle.state == Battle.BattleState.STARTING:
                LogUtils.info(f"A round has now passed with combat engaged for: {p.name}, FIGHT!", self.logger)
                battle.state = Battle.BattleState.INPROGRESS
            elif battle.state == Battle.BattleState.INPROGRESS:
                round = await self.calculate_monster_damage(round, p, battle.room)    
            elif battle.state == Battle.BattleState.COMPLETED:
                LogUtils.info(f"{method_name}: The battle has ended!", self.logger)
            elif battle.state == Battle.BattleState.RECORDED:
                LogUtils.info(f"{method_name}: The battle has been recorded in history!", self.logger)
                battle = None
            elif p.room.monsters == []:
                LogUtils.info(f"{method_name}: No monsters in room, stopping all battles", self.logger)
                if battle.state != Battle.BattleState.COMPLETED:
                    battle.state = Battle.BattleState.COMPLETED 
            else:
                LogUtils.error(f"{method_name}: WHY ARE WE HERE?", self.logger)

            # no point in continuing if player is dead..
            p.hitpoints -= round.damage_dealt
            if p.hitpoints <= 0:                    
                p, world = await p.you_died(world)
                    
                 # stop battle too
                for monster in p.previous_room.monsters:
                    await monster.stop_combat(p)

                battle.room.players.remove(p)
                if battle.room.players == []:
                    if battle.state == Battle.BattleState.CHECKING:
                        battle.state = Battle.BattleState.NONSTART
                    else:
                        battle.state = Battle.BattleState.COMPLETED
                
            # Updating health bar
            await p.send_health()

        if battle is not None:
            battle.rounds.append(round)
            
        LogUtils.debug(f"{method_name}: exit", self.logger)            
        return battle, world

    # calculate the round damage and sends messages to players
    async def calculate_monster_damage(self, round, player, room):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        total_damage = 0
        monsters_damage = []
        monsters_in_room = False
       
        # need to check here if combat is still going.. we may have killed everything or moved rooms
        for monster in room.monsters:
            monster.in_combat = random.choice(room.players)
            LogUtils.debug(f"{method_name}: ({monster.name}) is is_alive: {monster.is_alive} and in_combat:{monster.in_combat} and is attacking {monster.in_combat.name}", self.logger)
            
            # as we call this function by self.player, we need to only capture damage by player
            if monster.is_alive == True and monster.in_combat == player:
                monsters_in_room = True
                LogUtils.debug(
                    f'{method_name}: Monster "{monster.name}" is alive and is attacking {player.name}!',
                    self.logger,
                )

                # calculate our damage
                obj = monster.damage.split("d")
                dice = int(obj[0])
                damage_potential = int(obj[1])
                damage_multipler = random.randint(0, damage_potential)

                # roll dice for a monster
                damage = dice * damage_multipler
                total_damage += damage
                
                round.monsters.append(monster)
                round.damage_dealt += damage

                # add to our monster damage list
                monster_damage = dict(name=monster.name, damage=damage)
                monsters_damage.append(monster_damage)

        # sort based on damage
        monsters_damage = sorted(
            monsters_damage, key=lambda k: k["damage"], reverse=True
        )

        # build our attack message
        attack_msg = ""
        LogUtils.debug(f"{method_name}: Building our attack message. (total_damage: {total_damage}, monsters_damage: {monsters_damage})", self.logger)
        if len(room.monsters) == 1:
            attack_msg = f"{room.monsters[0].name} hit you for {total_damage} damage!"
        else:
            attack_msg = f"You have been wounded for {total_damage} damage!"
            attack_msg_extra = " ("
            for monster_damage in monsters_damage:
                if monster_damage["damage"] > 0:
                    attack_msg_extra += (
                        f"{monster_damage['name']}: {monster_damage['damage']}, "
                    )
            attack_msg_extra = attack_msg_extra[0 : len(attack_msg_extra) - 2]
            attack_msg_extra += ")"
            attack_msg = f"{attack_msg} {attack_msg_extra}"

        # send our attack messages
        if monsters_in_room == True:
            for p in room.players:
                if p.websocket == player.websocket:
                    if total_damage > 0:
                        await self.send_message(MudEvents.AttackEvent(attack_msg), p.websocket)
                    else:
                        await self.send_message(MudEvents.InfoEvent("You were dealt no damage this round!"), p.websocket)

                else:  # alert others of the battle
                    if total_damage > 0:
                        await self.send_message(MudEvents.InfoEvent(attack_msg.replace(
                            "You were", f"{player.name} was"
                        )), p.websocket)
                    else:
                        await self.send_message(MudEvents.InfoEvent(f"{player.name} was dealt no damage!"), p.websocket)

        LogUtils.debug(
            f"{method_name}: exit, returning round: {round}", self.logger
        )
        return round
