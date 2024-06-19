import inspect
import random
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility


class Combat:
    logger = None
    rounds = []
    
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug(f"Initializing Combat() class", self.logger)


    class CombatRound(Utility):
        in_combat = None
        room = None
        player_attacked = None

        def __init__(self, in_combat, room, player_attacked, logger):
            self.logger = logger
            self.in_combat = in_combat
            self.room = room
            self.player_attacked = player_attacked
            
            LogUtils.debug(f"Initializing PreviousRound() class", self.logger)

    # every two seconds this method is called
    # it will check to see if the monster is still in combat
    async def run_combat_round(self, combats_in_progress, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)  
        for player in world.players.players:
            room = await world.rooms.get_room(player.location_id)
            for monster in room.monsters:
                if monster.is_alive == True:
                    LogUtils.debug(f'{method_name}: Monster "{monster.name}" is alive', self.logger)
                else:
                    LogUtils.debug(f'{method_name}: Monster "{monster.name}" is dead.  Skipping.', self.logger)
                    continue
                         
                # new combat
                if monster.in_combat == None: 
                    combats_in_progress.append(await self.start_fight(player, world))
                else:
                    # choose whether to keep fighting same person or switch
                    previous_round = monster.rounds[len(monster.rounds)-1]
                    if len(previous_round.room.players) == len(room.players):
                        monster.in_combat = previous_round.player_attacked
                    else:
                        monster.in_combat = random.choice(room.players)
                        LogUtils.debug(f"{method_name}: Monster ({monster.name}) is in combat and has switched to attacking {monster.in_combat.name}", self.logger)
                    
                    if monster.in_combat == monster.previous_combat:
                        monster.in_combat = random.choice(room.players)
                        if monster.in_combat == monster.previous_combat:
                            LogUtils.debug(
                                f"{method_name}: Monster ({monster.name}) is in combat and nothing has changed in the room to switch combat...",
                                self.logger,
                            )                                
                            await world.monsters.calculate_mob_damage(player, self)                                
                        else:
                            LogUtils.debug(
                                f"{method_name}: Monster ({monster.name}) is in combat and has switched to attacking {monster.in_combat.name}",
                                self.logger,
                            )

                monster.previous_combat = monster.in_combat
                self.CombatRound
                
                if monster.in_combat != None:
                    self.monsters_fighting.append(monster)
        LogUtils.debug(f"{method_name}: exit", self.logger)            
        return combats_in_progress

                                    
    async def start_fight(self, player_being_attacked, world):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)        
        room = world.rooms[player_being_attacked.location_id]
        
        # if monster is not attacking anyone, pick someone
        self.in_combat = random.choice(room.players)
        LogUtils.debug(f'{method_name}: "{self.name}" is not attacking anyone.  Now attacking {self.in_combat.name}', self.logger)   
        await self.alert_room(f"{self.name} stirs.", self, event_type=MudEvents.InfoEvent)                         
        if self.in_combat == player_being_attacked:
            await self.alert_room(f"{self.name} prepares to attack you!", self, event_type=MudEvents.AttackEvent, exclude_player=True, player=player_being_attacked)
        else:
            await self.alert_room(f"{self.name} prepares to attack {self.in_combat.name}.", self, event_type=MudEvents.InfoEvent, exclude_player=True, player=player_being_attacked)
        round = self.CombatRound(self, room, player_attacked = player_being_attacked)
        LogUtils.debug(f"{method_name}: exit, monster_round: {round}", self.logger)
        return round
        